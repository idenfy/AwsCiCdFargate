from typing import List, Dict, Any, Optional
from aws_cdk import aws_ec2


class EcsParams:
    """
    Parameters class which specifies deployed container and ecs parameters such as name, port, etc.
    """
    def __init__(
            self,
            container_name: str,
            container_cpu: int,
            container_ram: int,
            container_port: int,
            container_environment: Dict[str, Any],
            ecs_security_groups: List[aws_ec2.SecurityGroup],
            ecs_subnets: List[aws_ec2.Subnet],
            cpu_threshold: int = 50,
            healthy_http_codes: Optional[List[int]] = None,
            health_check_path: Optional[str] = None,

    ) -> None:
        """
        Constructor.

        :param container_name: The name that will be given to a newly deployed container.
        :param container_cpu: Cpu units for the deployed container. 1 CPU = 1024 Cpu units.
        :param container_ram: Memory for the deployed container. 1 GB Ram = 1024 units.
        :param container_port: An open container port through which a loadbalancer can communicate.
        :param container_environment: Environment that will be passed to a running container.
        :param ecs_security_groups: Security groups for ecs service in which containers are placed.
        :param ecs_subnets: Subnets to which new containers will be deployed.
        :param cpu_threshold: Measured in percent. 0-100 percent. This value indicates when an autoscaling should
        kick in. If an average containers' cpu utilization is below this threshold, the amount of servers should be
        decreased. On the contrary, if an average containers' cpu utilization is above this threshold, the amount
        of servers will be increased.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        :param health_check_path: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a path for that ping.

        :return: No return.
        """
        self.container_name = container_name
        self.container_cpu = container_cpu
        self.container_ram = container_ram
        self.container_port = container_port
        self.container_environment = container_environment
        self.ecs_security_groups = ecs_security_groups
        self.ecs_subnets = ecs_subnets
        self.cpu_threshold = cpu_threshold
        self.healthy_http_codes = healthy_http_codes
        self.health_check_path = health_check_path
