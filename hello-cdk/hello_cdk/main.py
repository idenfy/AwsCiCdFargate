from typing import List, Dict, Optional

from aws_cdk import core, aws_ecs, aws_codedeploy, aws_codecommit, aws_codebuild, aws_codepipeline, \
    aws_codepipeline_actions, aws_ecr, aws_ecs_patterns, aws_elasticloadbalancingv2, aws_ec2, aws_certificatemanager, aws_iam, aws_s3, aws_ec2
from aws_cdk.custom_resources import AwsCustomResource

from hello_cdk.ecs_loadbalancer import Loadbalancing
from hello_cdk.ecs_main import Ecs


class EcsParams:
    """
    Parameters class which specifies deployed container and ecs parameters such as name, port, etc.
    """
    def __init__(
            self,
            container_name: str,
            container_cpu: str,
            container_ram: str,
            container_port: int,
            container_environment: Dict[str, any],
            ecs_security_groups: List[aws_ec2.SecurityGroup],
            ecs_subnets: List[aws_ec2.Subnet]
    ) -> None:
        """
        Constructor.
        :param container_name: The name that will be given to a newly deployed container.
        :param container_cpu: Cpu points for the deployed container. 1 CPU = 1024 Cpu units.
        :param container_ram: Memory for the deployed container. 1 GB Ram = 1024 units.
        :param container_port: An open container port through which a loadbalancer can communicate.
        :param container_environment: Environment that will be passed to a running container.
        :param ecs_security_groups: Security groups for ecs service in which containers are placed.
        :param ecs_subnets: Subnets to which new containers will be deployed.
        """
        self.container_name = container_name
        self.container_cpu = container_cpu
        self.container_ram = container_ram
        self.container_port = container_port
        self.container_environment = container_environment
        self.ecs_security_groups = ecs_security_groups
        self.ecs_subnets = ecs_subnets


class LoadBalancerParams():
    def __init__(
            self,
            subnets: List[aws_ec2.Subnet],
            security_groups: List[aws_ec2.SecurityGroup],
            dns: str,
            healthy_http_codes: Optional[List[int]] = None
    ):
        """
        Constructor.
        :param subnet: Subnets in which a newly created loadbalancer can operate.
        :param dns: A domain name for a loadbalancer. E.g. myweb.com. This is used to issue a new
        certificate in order a loadbalancer can use HTTPS connections.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        """
        self.dns = dns
        self.security_groups = security_groups
        self.lb_subnets = subnets
        self.healthy_http_codes = healthy_http_codes


class Main:
    TARGET_GROUP_PORT = 80
    LISTENER_HTTP_PORT_1 = 80
    LISTENER_HTTPS_PORT_1 = 443
    LISTENER_HTTP_PORT_2 = 8000
    LISTENER_HTTPS_PORT_2 = 44300

    def __init__(
            self,
            prefix: str,
            vpc: aws_ec2.Vpc,
            lb_params: LoadBalancerParams,
            ecs_params: EcsParams,
    ) -> None:
        """
        Constructor.
        :param prefix: The prefix for all newly created resources. E.g. Wordpress.
        :param region: The region where resources and the stack are deployed.
        :param account_id: The id of the account which executes this stack.
        :param vpc: Virtual private cloud (VPC).
        :param lb_params: Loadbalancer parameters.
        :param ecs_params: Compute power parameters for newly deployed container.
        :param pipeline_params: Parameters for a ci/cd pipeline.
        """

        self.load_balancing = Loadbalancing(
            prefix=prefix,
            subnets=lb_params.lb_subnets,
            lb_security_groups=lb_params.security_groups,
            vpc=vpc,
            desired_domain_name=lb_params.dns,
            healthy_http_codes=lb_params.healthy_http_codes
        )

        # Create main fargate ecs service.
        self.ecs = Ecs(
            prefix=prefix,
            # environment=ecs_params.container_environment,
            cpu=ecs_params.container_cpu,
            ram=ecs_params.container_ram,
            container_name=ecs_params.container_name,
            loadbalancing=self.load_balancing
        )

