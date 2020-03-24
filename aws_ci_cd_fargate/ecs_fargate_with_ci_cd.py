from aws_cdk import aws_ec2
from aws_ci_cd_fargate.parameters.lb_listener_parameters import LbListenerParameters
from aws_ci_cd_fargate.parameters.pipeline_parameters import PipelineParams
from aws_ci_cd_fargate.source.ecs_main import Ecs
from aws_ci_cd_fargate.source.ecs_pipeline import EcsPipeline
from aws_ci_cd_fargate.parameters.ecs_parameters import EcsParams
from aws_ci_cd_fargate.parameters.load_balancer_parameters import LoadBalancerParams
from aws_ci_cd_fargate.source.lb_listener_config import LbListenerConfig


class EcsFargateWithCiCd:
    """
    Creates a whole infrastructure around ECS Fargate service and blue/green CI/CD deployments.
    """
    def __init__(
            self,
            scope,
            prefix: str,
            vpc: aws_ec2.Vpc,
            lb_params: LoadBalancerParams,
            ecs_params: EcsParams,
            lb_listener_params: LbListenerParameters,
            pipeline_params: PipelineParams
    ) -> None:
        """
        Constructor.

        :param scope: A CF stack in which to create resources.
        :param prefix: The prefix for all newly created resources. E.g. Wordpress.
        :param vpc: Virtual private cloud (VPC).
        :param lb_params: Loadbalancer parameters.
        :param ecs_params: Compute power parameters for newly deployed container.
        :param lb_listener_params: Parameters two configure existing listeners with listener rules.
        :param pipeline_params: Configuration parameters for ci/cd pipeline.
        """
        self.lb_listener_config = LbListenerConfig(
            scope,
            prefix=prefix,
            vpc=vpc,
            listener_params=lb_listener_params,
            healthy_http_codes=lb_params.healthy_http_codes,
            health_check_path=lb_params.health_check_path
        )

        self.ecs = Ecs(
            scope,
            prefix=prefix,
            ecs_params=ecs_params,
            lb_listener_config=self.lb_listener_config,
            vpc=vpc
        )

        self.pipeline = EcsPipeline(
            scope,
            prefix=prefix,
            main_listener=lb_listener_params.production_listener,
            deployments_listener=lb_listener_params.deployment_listener,
            ecs_service=self.ecs.service,
            ecs_cluster=self.ecs.cluster,
            task_def=self.ecs.create_task_def(),
            app_spec=self.ecs.create_appspec(),
            build_environment=pipeline_params.build_environment,
            docker_build_args=pipeline_params.docker_build_args,
            production_target_group=self.lb_listener_config.production_target_group,
            deployment_target_group=self.lb_listener_config.deployment_target_group
        )
