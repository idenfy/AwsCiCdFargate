from typing import List, Optional

from aws_cdk import aws_certificatemanager, aws_elasticloadbalancingv2, core
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
            scope,
            prefix: str,
            lb_security_groups: List[SecurityGroup],
            subnets: List[Subnet],
            vpc: Vpc,
            desired_domain_name: str,
            healthy_http_codes: Optional[List[int]] = None,
            health_check_path: Optional[str] = None
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

        healthy_http_codes = [str(code) for code in healthy_http_codes] if healthy_http_codes else ['200']
        # By default a healthy http code is considered to be 200.
        healthy_http_codes = ','.join(healthy_http_codes)

        # If your service's task definition uses the awsvpc network mode
        # (which is required for the Fargate launch type), you must choose ip as the target type,
        # not instance, when creating your target groups because
        # tasks that use the awsvpc network mode are associated with an elastic network interface,
        # not an Amazon EC2 instance.
        # self.target_type = aws_elasticloadbalancingv2.TargetType.IP
        self.target_type = 'ip'
        self.certificate = aws_certificatemanager.CfnCertificate(
            scope, prefix + 'FargateEcsCertificate',
            domain_name=desired_domain_name,
            validation_method='EMAIL'
        )

        self.target_group_1_http = aws_elasticloadbalancingv2.CfnTargetGroup(
            scope, prefix + 'FargateEcsTargetGroup1',
            name=prefix + 'FargateEcsTargetGroup1',
            matcher=aws_elasticloadbalancingv2.CfnTargetGroup.MatcherProperty(http_code=healthy_http_codes),
            port=self.TARGET_GROUP_PORT,
            protocol='HTTP',
            vpc_id=vpc.vpc_id,
            target_type=self.target_type,
            health_check_path=health_check_path if health_check_path else '/'
        )

        self.target_group_2_http = aws_elasticloadbalancingv2.CfnTargetGroup(
            scope, prefix + 'FargateEcsTargetGroup2',
            name=prefix + 'FargateEcsTargetGroup2',
            matcher=aws_elasticloadbalancingv2.CfnTargetGroup.MatcherProperty(http_code=healthy_http_codes),
            port=self.TARGET_GROUP_PORT,
            protocol='HTTP',
            vpc_id=vpc.vpc_id,
            target_type=self.target_type,
            health_check_path=health_check_path if health_check_path else '/'
        )

        self.load_balancer = aws_elasticloadbalancingv2.CfnLoadBalancer(
            scope, prefix + 'FargateEcsLoadBalancer',
            security_groups=[group.security_group_id for group in lb_security_groups],
            subnets=[subnet.subnet_id for subnet in subnets],
            type='application',
            scheme='internet-facing',
            name=prefix + 'FargateEcsLoadBalancer'
        )

        self.load_balancer_output = core.CfnOutput(
            scope, prefix + 'FargateEcsLoadBalancerUrl',
            description='The endpoint url of a loadbalancer.',
            value=self.load_balancer.attr_dns_name
        )

        self.listener_http_1 = aws_elasticloadbalancingv2.CfnListener(
            scope, prefix + 'FargateEcsHttpListener1',
            port=self.LISTENER_HTTP_PORT_1,
            protocol='HTTP',
            load_balancer_arn=self.load_balancer.ref,
            default_actions=[
                aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty(
                        status_code='HTTP_301',
                        host='#{host}',
                        path='/#{path}',
                        port=str(self.LISTENER_HTTPS_PORT_1),
                        query='#{query}',
                        protocol='HTTPS'
                    )
                )
            ]
        )

        self.listener_https_1 = aws_elasticloadbalancingv2.CfnListener(
            scope, prefix + 'FargateEcsHttpsListener1',
            certificates=[aws_elasticloadbalancingv2.CfnListener.CertificateProperty(
                certificate_arn=self.certificate.ref
            )],
            port=self.LISTENER_HTTPS_PORT_1,
            protocol='HTTPS',
            load_balancer_arn=self.load_balancer.ref,
            default_actions=[
                aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='forward',
                    target_group_arn=self.target_group_1_http.ref
                )
            ]
        )

        self.listener_http_2 = aws_elasticloadbalancingv2.CfnListener(
            scope, prefix + 'FargateEcsHttpListener2',
            port=self.LISTENER_HTTP_PORT_2,
            protocol='HTTP',
            load_balancer_arn=self.load_balancer.ref,
            default_actions=[
                aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty(
                        status_code='HTTP_301',
                        host='#{host}',
                        path='/#{path}',
                        port=str(self.LISTENER_HTTPS_PORT_2),
                        query='#{query}',
                        protocol='HTTPS'
                    )
                )
            ]
        )

        self.listener_https_2 = aws_elasticloadbalancingv2.CfnListener(
            scope, prefix + 'FargateEcsHttpsListener2',
            certificates=[aws_elasticloadbalancingv2.CfnListener.CertificateProperty(
                certificate_arn=self.certificate.ref
            )],
            port=self.LISTENER_HTTPS_PORT_2,
            protocol='HTTPS',
            load_balancer_arn=self.load_balancer.ref,
            default_actions=[
                aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='forward',
                    target_group_arn=self.target_group_2_http.ref
                )
            ]
        )

