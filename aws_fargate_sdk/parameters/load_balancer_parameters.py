from typing import Optional
from aws_cdk import aws_ec2, aws_certificatemanager, aws_elasticloadbalancingv2


class LoadBalancerParams:
    def __init__(
            self,
            loadbalancer: aws_elasticloadbalancingv2.CfnLoadBalancer,
            security_group: aws_ec2.ISecurityGroup,
            certificate: Optional[aws_certificatemanager.CfnCertificate] = None
    ) -> None:

        self.loadbalander = loadbalancer
        self.security_group = security_group
        self.certificate = certificate
