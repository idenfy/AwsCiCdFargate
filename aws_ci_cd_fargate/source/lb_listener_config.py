from typing import List, Optional
from aws_cdk import aws_elasticloadbalancingv2
from aws_cdk.aws_ec2 import Vpc
from aws_ci_cd_fargate.parameters.lb_listener_parameters import LbListenerParameters


class LbListenerConfig:
    """
    Class which configures loabalancer's listeners to support blue-green deployments.
    """
    TARGET_GROUP_PORT = 80

    def __init__(
            self,
            scope,
            prefix: str,
            vpc: Vpc,
            listener_params: LbListenerParameters,
            healthy_http_codes: Optional[List[int]] = None,
            health_check_path: Optional[str] = None
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation template to which add resources.
        :param prefix: A prefix for resource names.
        :param vpc: Virtual private cloud in which target groups and a loadbalancer exist.
        :param listener_params: Configuration parameters for loadbalancer's listeners.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        :param health_check_path: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a path to ping.
        """
        # By default a healthy http code is considered to be 200.
        healthy_http_codes = [str(code) for code in healthy_http_codes] if healthy_http_codes else ['200']
        healthy_http_codes = ','.join(healthy_http_codes)

        # If your service's task definition uses the awsvpc network mode
        # (which is required for the Fargate launch type), you must choose ip as the target type,
        # not instance, when creating your target groups because
        # tasks that use the awsvpc network mode are associated with an elastic network interface,
        # not an Amazon EC2 instance.
        # self.target_type = aws_elasticloadbalancingv2.TargetType.IP
        self.target_type = 'ip'

        """
        PRODUCTION CONFIG
        """

        self.production_target_group = aws_elasticloadbalancingv2.CfnTargetGroup(
            scope,
            prefix + 'FargateProdTG',
            name=prefix + 'FargateProdTG',
            matcher=aws_elasticloadbalancingv2.CfnTargetGroup.MatcherProperty(http_code=healthy_http_codes),
            port=self.TARGET_GROUP_PORT,
            protocol='HTTP',
            vpc_id=vpc.vpc_id,
            target_type=self.target_type,
            health_check_path=health_check_path if health_check_path else '/'
        )

        self.production_rule = aws_elasticloadbalancingv2.CfnListenerRule(
            scope=scope,
            id=prefix + 'ProductionListenerRule',
            actions=[
                aws_elasticloadbalancingv2.CfnListenerRule.ActionProperty(
                    type='forward',
                    target_group_arn=self.production_target_group.ref
                )
            ],
            conditions=[
                listener_params.rule_condition
            ],
            listener_arn=listener_params.production_listener.ref,
            priority=listener_params.rule_priority
        )

        """
        DEPLOYMENT CONFIG
        """

        self.deployment_target_group = aws_elasticloadbalancingv2.CfnTargetGroup(
            scope, prefix + 'FargateDeplTG',
            name=prefix + 'FargateDeplTG',
            matcher=aws_elasticloadbalancingv2.CfnTargetGroup.MatcherProperty(http_code=healthy_http_codes),
            port=self.TARGET_GROUP_PORT,
            protocol='HTTP',
            vpc_id=vpc.vpc_id,
            target_type=self.target_type,
            health_check_path=health_check_path if health_check_path else '/'
        )

        self.deployment_rule = aws_elasticloadbalancingv2.CfnListenerRule(
            scope=scope,
            id=prefix + 'DeploymentListenerRule',
            actions=[
                aws_elasticloadbalancingv2.CfnListenerRule.ActionProperty(
                    type='forward',
                    target_group_arn=self.deployment_target_group.ref
                )
            ],
            conditions=[
                listener_params.rule_condition
            ],
            listener_arn=listener_params.deployment_listener.ref,
            priority=listener_params.rule_priority
        )
