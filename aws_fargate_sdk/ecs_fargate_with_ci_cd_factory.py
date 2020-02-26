from typing import Optional, List
from aws_cdk import aws_elasticloadbalancingv2, aws_certificatemanager
from aws_cdk.aws_ec2 import IVpc
from aws_cdk.core import Stack
from aws_cdk import aws_ec2, aws_elasticloadbalancingv2, aws_certificatemanager
from aws_fargate_sdk.ecs_fargate_with_ci_cd import EcsFargateWithCiCd
from aws_fargate_sdk.parameters.ecs_parameters import EcsParams
from aws_fargate_sdk.parameters.load_balancer_parameters import LoadBalancerParams
from aws_fargate_sdk.security_group_modifier import SecurityGroupModifier


class EcsFargateWithCiCdFactory:
    """
    Creates a whole infrastructure around ECS Fargate service and blue/green CI/CD deployments.
    """
    def __init__(
            self,
            scope,
            vpc: aws_ec2.Vpc,
            lb_params: LoadBalancerParams,
    ) -> None:
        """
        Constructor.
        :param vpc: Virtual private cloud (VPC).
        :param lb_params: Loadbalancer parameters.
        """

        self.__scope = scope
        self.__vpc = vpc
        self.__loadbalancer = lb_params.loadbalander
        self.__available_ports = list(range(10000, 25000))

        self.__lb_params = lb_params

        self.__security_group_modifier = SecurityGroupModifier(lb_params.security_group)

    def create(self, ecs_params: EcsParams, prefix: str):

        production_target_group = self.__create_target_group(
            prefix,
            self.__vpc,
            'FargateProdTG',
            ecs_params.healthy_http_codes,
            ecs_params.health_check_path,
        )

        deployment_target_group = self.__create_target_group(
            prefix,
            self.__vpc,
            'FargateDeplTG',
            ecs_params.healthy_http_codes,
            ecs_params.health_check_path,
        )

        production_listener = self.__create_listener(
            prefix,
            self.__lb_params.certificate,
            aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='forward',
                    target_group_arn=production_target_group
            )
        )

        deployments_listener = self.__create_listener(
            prefix,
            self.__lb_params.certificate,
            aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                type='forward',
                target_group_arn=production_target_group
            )
        )

        if self.__lb_params.certificate is not None:
            self.__create_listener(
                prefix,
                action=aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty(
                        status_code='HTTP_301',
                        host='#{host}',
                        path='/#{path}',
                        port=str(production_listener.port),
                        query='#{query}',
                        protocol='HTTPS'
                    )
                )
            )

            self.__create_listener(
                prefix,
                action=aws_elasticloadbalancingv2.CfnListener.ActionProperty(
                    type='redirect',
                    redirect_config=aws_elasticloadbalancingv2.CfnListener.RedirectConfigProperty(
                        status_code='HTTP_301',
                        host='#{host}',
                        path='/#{path}',
                        port=str(deployments_listener.port),
                        query='#{query}',
                        protocol='HTTPS'
                    )
                )
            )

        EcsFargateWithCiCd(
            self.__scope,
            prefix,
            self.__vpc,
            ecs_params,
            production_target_group,
            deployment_target_group,
            production_listener,
            deployments_listener
        )

    def __create_listener(
            self,
            prefix: str,
            certificate: Optional[aws_certificatemanager.CfnCertificate] = None,
            action: Optional[aws_elasticloadbalancingv2.CfnListener.ActionProperty] = None
    ) -> aws_elasticloadbalancingv2.CfnListener:

        port = self.__allocate_port()
        self.__security_group_modifier.open_port(port, aws_ec2.Peer.any_ipv4())

        listener = aws_elasticloadbalancingv2.CfnListener(
            self.__scope,
            prefix + f'HttpsListener{port}',
            port=port,
            protocol='HTTPS' if certificate else 'HTTP',
            load_balancer_arn=self.__loadbalancer.ref,
            default_actions=[
                action or self.__default_404_action()
            ]
        )
        if certificate:
            listener.certificates = [
                aws_elasticloadbalancingv2.CfnListener.CertificateProperty(
                    certificate_arn=certificate.ref
                )
            ]
        return listener

    def __create_target_group(
            self,
            prefix: str,
            vpc: IVpc,
            name: str,
            healthy_http_codes: Optional[List[int]] = None,
            health_check_path: Optional[str] = None,
            target_group_port: int = 80,
            protocol: str = 'HTTP',
            target_type: str = 'ip',
    ) -> aws_elasticloadbalancingv2.CfnTargetGroup:
        # By default a healthy http code is considered to be 200.
        healthy_http_codes = [str(code) for code in healthy_http_codes] if healthy_http_codes else ['200']
        healthy_http_codes = ','.join(healthy_http_codes)

        return aws_elasticloadbalancingv2.CfnTargetGroup(
            self.__scope,
            prefix + name,
            name=prefix + name,
            matcher=aws_elasticloadbalancingv2.CfnTargetGroup.MatcherProperty(http_code=healthy_http_codes),
            port=target_group_port,
            protocol=protocol,
            vpc_id=vpc.vpc_id,
            target_type=target_type,
            health_check_path=health_check_path if health_check_path else '/'
        )

    @staticmethod
    def __default_404_action() -> aws_elasticloadbalancingv2.CfnListener.ActionProperty:
        return aws_elasticloadbalancingv2.CfnListener.ActionProperty(
            type='fixed-response',
            fixed_response_config=aws_elasticloadbalancingv2.CfnListener.FixedResponseConfigProperty(
                status_code='404',
                message_body='Not found.'
            )
        )

    def __allocate_port(self) -> int:
        return self.__available_ports.pop(0)

