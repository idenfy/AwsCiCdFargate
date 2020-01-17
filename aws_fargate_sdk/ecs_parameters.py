from typing import List, Dict, Any
from aws_cdk import aws_ec2

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
            container_environment: Dict[str, Any],
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