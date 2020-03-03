import json

from typing import List, Dict, Any
from aws_cdk import aws_logs, aws_ecs, aws_applicationautoscaling, aws_ec2, aws_iam,  custom_resources
from aws_cdk.aws_ec2 import SecurityGroup, Subnet
from aws_cdk.core import Stack, RemovalPolicy

from aws_fargate_sdk.source.lb_listener_config import LbListenerConfig


class Ecs:
    """
    Class that creates ECS Fargate service.
    """
    def __init__(
            self,
            scope: Stack,
            prefix: str,
            cpu: str,
            ram: str,
            cpu_threshold: int,
            environment: Dict[str, Any],
            container_name: str,
            container_port: int,
            security_groups: List[SecurityGroup],
            subnets: List[Subnet],
            lb_listener_config: LbListenerConfig,
            vpc: aws_ec2.Vpc
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation template to which add resources.
        :param prefix: A prefix for newly created resources.
        :param cpu: Cpu points for the deployed container. 1 CPU = 1024 Cpu points.
        :param ram: Memory for the deployed container. 1 GB Ram = 1024.
        :param cpu_threshold: Measured in percent. 0-100 percent. This value indicates when an autoscaling should
        kick in. If an average containers' cpu utilization is below this threshold, the amount of servers should be
        decreased. On the contrary, if an average containers' cpu utilization is above this threshold, the amount
        of servers will be increased.
        :param environment: A containers environment. Usually used for configuration an passing passwords.
        :param container_name: The name that will be given to a newly deployed container.
        :param container_port: A port through which ECS service can communicate.
        :param security_groups: Security groups for the ECS service.
        :param subnets: Subnets to deploy containers.
        :param vpc: Virtual Private Cloud in which loadbalancer and other instances are/will be located.
        """
        self.prefix = prefix
        self.aws_region = scope.region
        self.environment = environment
        self.cpu = cpu
        self.ram = ram
        self.container_name = container_name
        self.container_port = container_port

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

        self.cluster = aws_ecs.Cluster(
            scope, prefix + 'FargateCluster',
            cluster_name=prefix + 'FargateCluster',
            vpc=vpc
        )

        self.task = aws_ecs.FargateTaskDefinition(
            scope, prefix + 'FargateTaskDefinition',
            cpu=int(cpu), memory_limit_mib=int(ram), family=prefix.lower(),
            execution_role=self.task_execution_role
        )

        self.container = self.task.add_container(
            container_name,
            image=aws_ecs.ContainerImage.from_registry('eexit/mirror-http-server:latest'),
            logging=aws_ecs.AwsLogDriver(stream_prefix=prefix, log_group=self.log_group)
        )
        self.container.add_port_mappings(aws_ecs.PortMapping(container_port=80))

        self.service = custom_resources.AwsCustomResource(
            scope, prefix + 'FargateService',
            on_create={
                "service": 'ECS',
                "action": 'createService',
                "physical_resource_id": self.prefix + 'FargateServiceCustom',
                'parameters': {
                    'cluster': self.cluster.cluster_arn,
                    'serviceName': prefix + 'FargateService',
                    'taskDefinition': self.task.task_definition_arn,
                    'loadBalancers': [
                        {
                            'containerName': container_name,
                            'containerPort': container_port,
                            'targetGroupArn': lb_listener_config.production_target_group.ref
                        }
                    ],
                    'desiredCount': 1,
                    'networkConfiguration': {
                        'awsvpcConfiguration': {
                            'assignPublicIp': 'DISABLED',
                            'securityGroups': [sub.security_group_id for sub in security_groups],
                            'subnets': [sub.subnet_id for sub in subnets],
                        }
                    },
                    'deploymentController': {
                        'type': 'CODE_DEPLOY'
                    },
                    'launchType': 'FARGATE'
                }
            },
            on_delete={
                "service": 'ECS',
                "action": 'deleteService',
                "physical_resource_id": self.prefix + 'FargateServiceCustom',
                'parameters': {
                    'cluster': self.cluster.cluster_arn,
                    'service': prefix + 'FargateService',
                    'force': True
                }
            }
        )

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
            target_value=cpu_threshold,
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
                    'name': self.container_name,
                    'image': "<IMAGE1_NAME>",
                    'essential': True,
                    'environment': [
                        {'name': key, 'value': value} for key, value in self.environment.items()
                    ],
                    'portMappings': [
                        {
                            'containerPort': self.container_port
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
            'cpu': str(self.cpu),
            'memory': str(self.ram),
            'family': self.prefix.lower()
        }

        return json.dumps(definition, indent=4)
