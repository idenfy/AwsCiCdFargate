from aws_cdk import aws_ec2, core
from .ecs_loadbalancer import Loadbalancing
from .ecs_main import Ecs
from .ecs_pipeline import EcsPipeline
from .ecs_parameters import EcsParams
from .load_balancer_parameters import LoadBalancerParams
from .pipeline_parameters import PipelineParams


class Main:
    TARGET_GROUP_PORT = 80
    LISTENER_HTTP_PORT_1 = 80
    LISTENER_HTTPS_PORT_1 = 443
    LISTENER_HTTP_PORT_2 = 8000
    LISTENER_HTTPS_PORT_2 = 44300

    def __init__(
            self,
            scope,
            prefix: str,
            vpc: aws_ec2.Vpc,
            lb_params: LoadBalancerParams,
            ecs_params: EcsParams,
            pipeline_params: PipelineParams,
            region: str,
    ) -> None:
        """
        Constructor.
        :param prefix: The prefix for all newly created resources. E.g. Wordpress.
        :param region: The region where resources and the stack are deployed.
        :param vpc: Virtual private cloud (VPC).
        :param lb_params: Loadbalancer parameters.
        :param ecs_params: Compute power parameters for newly deployed container.
        :param pipeline_params: Parameters for a ci/cd pipeline.
        """

        self.load_balancing = Loadbalancing(
            scope,
            prefix=prefix,
            subnets=lb_params.lb_subnets,
            lb_security_groups=lb_params.security_groups,
            vpc=vpc,
            desired_domain_name=lb_params.dns,
            healthy_http_codes=lb_params.healthy_http_codes
        )

        self.ecs = Ecs(
            scope,
            prefix=prefix,
            environment=ecs_params.container_environment,
            cpu=ecs_params.container_cpu,
            ram=ecs_params.container_ram,
            container_name=ecs_params.container_name,
            container_port=ecs_params.container_port,
            loadbalancing=self.load_balancing,
            security_groups=ecs_params.ecs_security_groups,
            subnets=ecs_params.ecs_subnets,
            aws_region=region,
            vpc=vpc
        )

        self.pipeline = EcsPipeline(
            scope,
            prefix=prefix,
            main_listener=self.load_balancing.listener_https_1,
            deployments_listener=self.load_balancing.listener_https_2,
            ecs_service=self.ecs.service,
            ecs_cluster=self.ecs.cluster,
            artifact_builds_s3=pipeline_params.artifact_builds_bucket,
            task_def=self.ecs.create_task_def(),
            app_spec=self.ecs.create_appspec(),
            aws_region=region,
        )
