from aws_cdk import aws_logs, aws_ecs, aws_ecs_patterns
from ecs_loadbalancer import Loadbalancing


class Ecs:
    """
    Class that creates ECS Fargate service.
    """
    def __init__(
            self,
            prefix: str,
            cpu: str,
            ram: str,
            container_name: str,
            loadbalancing: Loadbalancing
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

        self.log_group = aws_logs.LogGroup(
            self, prefix + 'FargateEcsLogGroup',
            log_group_name=f'/aws/ecs/fargate/{prefix}'
        )

        self.cluster = aws_ecs.Cluster(
            self, prefix + 'FargateEcsCluster',
            cluster_name=prefix + 'FargateEcsCluster'
        )

        self.task = aws_ecs.FargateTaskDefinition(
            self, prefix + 'FargateEcsTaskDefinition',
            cpu=int(cpu), memory_limit_mib=int(ram), family=prefix.lower(),

        )
        self.container = self.task.add_container(
            container_name,
            image=aws_ecs.ContainerImage.from_registry('nginx:latest'),
            logging=aws_ecs.AwsLogDriver(stream_prefix=prefix, log_group=self.log_group)
        )
        self.container.add_port_mappings(aws_ecs.PortMapping(container_port=80))
        self.service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Fargate",
            cluster=self.cluster,
            service_name=prefix + 'FargateEcsService',
            task_definition=self.task,
            load_balancer=loadbalancing.load_balancer,
            assign_public_ip=True,
        )
        self.scaling = self.service.service.auto_scale_task_count(max_capacity=5)
        self.scaling.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=75)

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

    def create_taskdef(self):
        pass
