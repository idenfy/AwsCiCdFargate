from typing import List, Optional
from aws_cdk import aws_ec2


class LoadBalancerParams:
    def __init__(
            self,
            subnets: List[aws_ec2.Subnet],
            security_groups: List[aws_ec2.SecurityGroup],
            dns: str,
            healthy_http_codes: Optional[List[int]] = None
    ):
        """
        Constructor.
        :param subnets: Subnets in which a newly created loadbalancer can operate.
        :param dns: A domain name for a loadbalancer. E.g. myweb.com. This is used to issue a new
        certificate in order a loadbalancer can use HTTPS connections.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        """
        self.dns = dns
        self.security_groups = security_groups
        self.lb_subnets = subnets
        self.healthy_http_codes = healthy_http_codes