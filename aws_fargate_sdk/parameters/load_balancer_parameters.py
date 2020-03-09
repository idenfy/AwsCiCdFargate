from typing import List, Optional
from aws_cdk import aws_ec2


class LoadBalancerParams:
    def __init__(
            self,
            healthy_http_codes: Optional[List[int]] = None,
            health_check_path: Optional[str] = None
    ) -> None:
        """
        Constructor.

        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        :param health_check_path: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a path for that ping.

        :return: No return.
        """
        self.healthy_http_codes: [List[int]] = healthy_http_codes or [200]
        self.health_check_path: str = health_check_path or '/'
