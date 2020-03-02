from aws_cdk import aws_ec2
from aws_fargate_sdk.source.ecs_main import Ecs
from aws_fargate_sdk.source.ecs_pipeline import EcsPipeline
from aws_fargate_sdk.parameters.ecs_parameters import EcsParams


class EcsFargateWithCiCd:
    """
    Creates a whole infrastructure around ECS Fargate service and blue/green CI/CD deployments.
    """
    def __init__(
            self,
            scope,
            prefix: str,
            vpc: aws_ec2.Vpc,
            ecs_params: EcsParams,
            production_target_group,
            deployment_target_group,
            production_listener,
            deployment_listener
    ) -> None:
        """
        Constructor.
        :param prefix: The prefix for all newly created resources. E.g. Wordpress.
        :param vpc: Virtual private cloud (VPC).
        :param ecs_params: Compute power parameters for newly deployed container.
        """

        self.ecs = Ecs(
            scope,
            prefix=prefix,
            environment=ecs_params.container_environment,
            cpu=ecs_params.container_cpu,
            ram=ecs_params.container_ram,
            cpu_threshold=ecs_params.cpu_threshold,
            container_name=ecs_params.container_name,
            container_port=ecs_params.container_port,
            security_groups=ecs_params.ecs_security_groups,
            subnets=ecs_params.ecs_subnets,
            production_target_group=production_target_group,
            deployment_target_group=deployment_target_group,
            vpc=vpc
        )

        self.pipeline = EcsPipeline(
            scope,
            prefix=prefix,
            main_listener=production_listener,
            deployments_listener=deployment_listener,
            production_target_group=production_target_group,
            deployment_target_group=deployment_target_group,
            ecs_service=self.ecs.service,
            ecs_cluster=self.ecs.cluster,
            task_def=self.ecs.create_task_def(),
            app_spec=self.ecs.create_appspec(),
        )
