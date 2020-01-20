from typing import List, Dict, Any
from aws_cdk import aws_logs, aws_ecs, aws_applicationautoscaling, aws_ec2, aws_iam
from aws_cdk.aws_ec2 import SecurityGroup, Subnet
from .ecs_loadbalancer import Loadbalancing


class Ecs:
    """
    Class that creates ECS Fargate service.
    """
    def __init__(
            self,
            scope,
            prefix: str,
            aws_region: str,
            cpu: str,
            ram: str,
            environment: Dict[str, Any],
            container_name: str,
            container_port: int,
            security_groups: List[SecurityGroup],
            subnets: List[Subnet],
            loadbalancing: Loadbalancing,
            vpc: aws_ec2.Vpc
    ) -> None:
        """
        Constructor.
        :param prefix: A prefix for newly created resources.
        :param aws_region: A region in which resources are put.
        :param cpu: Cpu points for the deployed container. 1 CPU = 1024 Cpu points.
        :param ram: Memory for the deployed container. 1 GB Ram = 1024.
        :param container_name: The name that will be given to a newly deployed container.
        created container will be associated with this group.
        """

        self.prefix = prefix
        self.aws_region = aws_region
        self.environment = environment
        self.cpu = cpu
        self.ram = ram
        self.container_name = container_name
        self.container_port = container_port

        self.task_execution_role = aws_iam.Role(
            scope, prefix + 'FargateEcsTaskExecutionRole',
            path='/',
            inline_policies={
                prefix + 'FargateEcsTaskExecutionPolicy': aws_iam.PolicyDocument(
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
            log_group_name=f'/aws/ecs/fargate/{prefix}'
        )

        self.cluster = aws_ecs.Cluster(
            scope, prefix + 'FargateEcsCluster',
            cluster_name=prefix + 'FargateEcsCluster',
            vpc=vpc
        )

        self.task = aws_ecs.FargateTaskDefinition(
            scope, prefix + 'FargateEcsTaskDefinition',
            cpu=int(cpu), memory_limit_mib=int(ram), family=prefix.lower(),
            execution_role=self.task_execution_role
        )
        self.container = self.task.add_container(
            container_name,
            image=aws_ecs.ContainerImage.from_registry('nginx:latest'),
            logging=aws_ecs.AwsLogDriver(stream_prefix=prefix, log_group=self.log_group)
        )
        self.container.add_port_mappings(aws_ecs.PortMapping(container_port=80))

        self.service = aws_ecs.CfnService(
            scope, prefix + 'FargateEcsService',
            cluster=self.cluster.cluster_arn,
            service_name=prefix + 'FargateEcsService',
            task_definition=self.task.task_definition_arn,
            load_balancers=[
                aws_ecs.CfnService.LoadBalancerProperty(
                    container_name=container_name,
                    container_port=container_port,
                    target_group_arn=loadbalancing.target_group_1_http.ref
                )
            ],
            desired_count=1,
            network_configuration=aws_ecs.CfnService.NetworkConfigurationProperty(
                awsvpc_configuration=aws_ecs.CfnService.AwsVpcConfigurationProperty(
                    assign_public_ip="DISABLED",
                    security_groups=[sub.security_group_id for sub in security_groups],
                    subnets=[sub.subnet_id for sub in subnets],
                )
            ),
            deployment_controller=aws_ecs.CfnService.DeploymentControllerProperty(
                type="CODE_DEPLOY"
            ),
            launch_type="FARGATE"
        )

        self.service.node.add_dependency(loadbalancing.load_balancer)
        self.service.node.add_dependency(loadbalancing.target_group_1_http)
        self.service.node.add_dependency(loadbalancing.target_group_2_http)
        self.service.node.add_dependency(loadbalancing.listener_http_1)
        self.service.node.add_dependency(loadbalancing.listener_http_2)
        self.service.node.add_dependency(loadbalancing.listener_https_1)
        self.service.node.add_dependency(loadbalancing.listener_https_2)

        self.scalable_target = aws_applicationautoscaling.ScalableTarget(
            scope, prefix + 'FargateEcsScalableTarget',
            min_capacity=1,
            max_capacity=5,
            service_namespace=aws_applicationautoscaling.ServiceNamespace.ECS,
            resource_id='/'.join(['service', self.cluster.cluster_name, prefix + 'FargateEcsService']),
            scalable_dimension='ecs:service:DesiredCount'
        )

        self.scalable_target.node.add_dependency(self.service)

        self.scaling_policy = aws_applicationautoscaling.TargetTrackingScalingPolicy(
            scope, prefix + 'FargateEcsScalingPolicy',
            policy_name=prefix + 'FargateEcsScalingPolicy',
            scaling_target=self.scalable_target,
            target_value=75.0,
            predefined_metric=aws_applicationautoscaling.PredefinedMetric.ECS_SERVICE_AVERAGE_CPU_UTILIZATION,
            disable_scale_in=False
        )

    def create_appspec(self):
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

    def create_task_def(self):
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

        return definition
