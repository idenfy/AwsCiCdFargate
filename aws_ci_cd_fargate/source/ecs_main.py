import json

from aws_cdk import aws_logs, aws_ecs, aws_applicationautoscaling, aws_ec2, aws_iam
from aws_cdk.core import Stack, RemovalPolicy
from aws_ci_cd_fargate.parameters.ecs_parameters import EcsParams
from aws_ci_cd_fargate.source.custom.ecs_service import EcsService
from aws_ci_cd_fargate.source.lb_listener_config import LbListenerConfig
from aws_ecs_cluster.ecs_cluster import EcsCluster

class Ecs:
    """
    Class that creates ECS Fargate service.
    """
    def __init__(
            self,
            scope: Stack,
            prefix: str,
            ecs_params: EcsParams,
            lb_listener_config: LbListenerConfig,
            vpc: aws_ec2.Vpc
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation template to which add resources.
        :param prefix: A prefix for newly created resources.
        :param ecs_params: Compute power parameters for newly deployed container.
        :param lb_listener_config: Listeners configuration for blue-green deployments.
        :param vpc: Virtual Private Cloud in which loadbalancer and other instances are/will be located.
        """
        self.prefix = prefix
        self.aws_region = scope.region
        self.ecs_params = ecs_params

        self.task_execution_role = aws_iam.Role(
            scope, prefix + 'FargateTaskExecutionRole',
            path='/',
            inline_policies={
                prefix + 'FargateTaskExecutionPolicy': aws_iam.PolicyDocument(
                    statements=[aws_iam.PolicyStatement(
                        actions=[
                            "ecr:GetAuthorizationToken",
                            "ecr:BatchCheckLayerAvailability",
                            "ecr:GetDownloadUrlForLayer",
                            "ecr:BatchGetImage",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents",
                            "cloudtrail:LookupEvents"
                        ],
                        resources=['*'],
                        effect=aws_iam.Effect.ALLOW)]
                )},
            assumed_by=aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
        )

        self.log_group = aws_logs.LogGroup(
            scope, prefix + 'FargateEcsLogGroup',
            log_group_name=f'/aws/ecs/fargate/{prefix}',
            removal_policy=RemovalPolicy.DESTROY
        )

        self.cluster = EcsCluster(
            scope, prefix + 'FargateCluster',
            cluster_name=prefix + 'FargateCluster',
            vpc=vpc
        )

        self.task = aws_ecs.FargateTaskDefinition(
            scope, prefix + 'FargateTaskDefinition',
            cpu=int(self.ecs_params.container_cpu), memory_limit_mib=int(self.ecs_params.container_ram), family=prefix.lower(),
            execution_role=self.task_execution_role
        )

        self.container = self.task.add_container(
            self.ecs_params.container_name,
            image=aws_ecs.ContainerImage.from_registry('eexit/mirror-http-server:latest'),
            logging=aws_ecs.AwsLogDriver(stream_prefix=prefix, log_group=self.log_group)
        )
        self.container.add_port_mappings(aws_ecs.PortMapping(container_port=80))

        self.service = EcsService(
            stack=scope,
            prefix=prefix,
            cluster=self.cluster,
            task=self.task,
            ecs_params=self.ecs_params,
            production_target_group=lb_listener_config.production_target_group
        ).get_resource().custom_resource

        self.service.node.add_dependency(lb_listener_config.production_target_group)
        self.service.node.add_dependency(lb_listener_config.deployment_target_group)

        self.scalable_target = aws_applicationautoscaling.ScalableTarget(
            scope, prefix + 'FargateScalableTarget',
            min_capacity=1,
            max_capacity=5,
            service_namespace=aws_applicationautoscaling.ServiceNamespace.ECS,
            resource_id='/'.join(['service', self.cluster.cluster_name, prefix + 'FargateService']),
            scalable_dimension='ecs:service:DesiredCount'
        )

        self.scalable_target.node.add_dependency(self.service)

        self.scaling_policy = aws_applicationautoscaling.TargetTrackingScalingPolicy(
            scope, prefix + 'FargateScalingPolicy',
            policy_name=prefix + 'FargateScalingPolicy',
            scaling_target=self.scalable_target,
            target_value=self.ecs_params.cpu_threshold,
            predefined_metric=aws_applicationautoscaling.PredefinedMetric.ECS_SERVICE_AVERAGE_CPU_UTILIZATION,
            disable_scale_in=False
        )

    def create_appspec(self) -> str:
        """
        Creates an application specification object which will be used for deploying new containers through a pipeline.
        The application specification object specifies parameters about the ECS service.

        :return: Application specification object.
        """
        app_spec = (
            f'version: 0.0',
            f'Resources:',
            f'  - TargetService:',
            f'      Type: AWS::ECS::Service',
            f'      Properties:',
            f'        TaskDefinition: <TASK_DEFINITION>',
            f'        LoadBalancerInfo:',
            f'          ContainerName: "{self.container.container_name}"',
            f'          ContainerPort: 80',
        )

        return '\n'.join(app_spec)

    def create_task_def(self) -> str:
        """
        Creates a task definition object which will be used for deploying new containers through a pipeline.
        The task definition object specifies parameters about newly created containers.

        :return: Task definition object.
        """
        definition = {
            'executionRoleArn': self.task.execution_role.role_arn,
            'containerDefinitions': [
                {
                    'name': self.ecs_params.container_name,
                    'image': "<IMAGE1_NAME>",
                    'essential': True,
                    'environment': [
                        {'name': key, 'value': value} for key, value in self.ecs_params.container_environment.items()
                    ],
                    'portMappings': [
                        {
                            'containerPort': 80
                        }
                    ],
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': self.log_group.log_group_name,
                            'awslogs-region': self.aws_region,
                            'awslogs-stream-prefix': self.prefix
                        }
                    }
                }
            ],
            'requiresCompatibilities': [
                'FARGATE'
            ],
            'networkMode': 'awsvpc',
            'cpu': str(self.ecs_params.container_cpu),
            'memory': str(self.ecs_params.container_ram),
            'family': self.prefix.lower()
        }

        return json.dumps(definition, indent=4)
