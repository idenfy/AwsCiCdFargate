from typing import List, Optional

from aws_cdk import aws_certificatemanager, aws_elasticloadbalancingv2
from aws_cdk.aws_ec2 import SecurityGroup, Subnet, Vpc


class Loadbalancing:
    """
    Class which creates a loadbalancer for ecs.
    """
    TARGET_GROUP_PORT = 80
    LISTENER_HTTP_PORT_1 = 80
    LISTENER_HTTPS_PORT_1 = 443
    LISTENER_HTTP_PORT_2 = 8000
    LISTENER_HTTPS_PORT_2 = 44300

    def __init__(
            self,
            prefix: str,
            lb_security_groups: List[SecurityGroup],
            subnets: List[Subnet],
            vpc: Vpc,
            desired_domain_name: str,
            healthy_http_codes: Optional[List[int]] = None
    ):
        """
        Constructor.

        :param prefix: A prefix for resource names.
        :param lb_security_groups: Security groups to attach to a loadbalancer. NOTE! when passing loadbalancer
        security groups - make sure the loadbalancer can communicate through ci/cd blue/green deployments
        opened ports. Usually they are 8000 and 44300.
        :param subnets: Subnets in which loadbalancer can exist.
        :param vpc: Virtual private cloud in which target groups and a loadbalancer exist.
        :param desired_domain_name: Domain name for using https.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        """
        # By default a healthy http code is considered to be 200.
        healthy_http_codes = healthy_http_codes or [200]

        # If your service's task definition uses the awsvpc network mode
        # (which is required for the Fargate launch type), you must choose ip as the target type,
        # not instance, when creating your target groups because
        # tasks that use the awsvpc network mode are associated with an elastic network interface,
        # not an Amazon EC2 instance.
        self.target_type = aws_elasticloadbalancingv2.TargetType.IP,

        self.certificate = aws_certificatemanager.Certificate(
            self, prefix + 'FargateEcsCertificate',
            domain_name=desired_domain_name,
            validation_method=aws_certificatemanager.ValidationMethod.DNS
        )

        self.load_balancer = aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, prefix + 'FargateEcsLoadBalancer',
            vpc=vpc,
            vpc_subnets=subnets,
            security_group=lb_security_groups
        )
        self.http_listener_1 = self.load_balancer.add_listener(
            prefix + 'FargateEcsHttpListener1',
            port=self.LISTENER_HTTP_PORT_1,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP
        )
        self.http_listener_1.add_redirect_response(
            'https-redirect',
            host='#{host}',
            path='/#{path}',
            port=str(self.LISTENER_HTTPS_PORT_1),
            query='#{query}',
            status_code='HTTP_301',
            protocol='HTTPS'
        )

        self.http_target_group_1 = aws_elasticloadbalancingv2.ApplicationTargetGroup(
            self, prefix + 'FargateEcsTargetGroup1',
            target_group_name=prefix + 'FargateEcsTargetGroup1',
            port=self.TARGET_GROUP_PORT,
            vpc=vpc,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            target_type=self.target_type,
            health_check=aws_elasticloadbalancingv2.HealthCheck()
        )

        self.https_listener_1 = self.load_balancer.add_listener(
            prefix + 'FargateEcsHttpsListener1',
            port=self.LISTENER_HTTPS_PORT_1,
            certificate_arns=[self.certificate.certificate_arn],
            default_target_groups=[self.http_target_group_1],
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS
        )

        self.http_listener_2 = self.load_balancer.add_listener(
            prefix + 'FargateEcsHttpListener2',
            port=self.LISTENER_HTTP_PORT_2,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP
        )

        self.http_listener_2.add_redirect_response(
            'https-redirect',
            host='#{host}',
            path='/#{path}',
            port=str(self.LISTENER_HTTPS_PORT_2),
            query='#{query}',
            status_code='HTTP_301',
            protocol='HTTPS'
        )

        self.http_target_group_2 = aws_elasticloadbalancingv2.ApplicationTargetGroup(
            self, prefix + 'FargateEcsTargetGroup2',
            target_group_name=prefix + 'FargateEcsTargetGroup2',
            port=self.TARGET_GROUP_PORT,
            vpc=vpc,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            target_type=self.target_type,
            health_check=aws_elasticloadbalancingv2.HealthCheck()
        )

        self.https_listener_2 = self.load_balancer.add_listener(
            prefix + 'FargateEcsHttpsListener2',
            port=self.LISTENER_HTTPS_PORT_2,
            certificate_arns=[self.certificate.certificate_arn],
            default_target_groups=[self.http_target_group_2],
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS
        )
