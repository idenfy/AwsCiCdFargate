from aws_cdk import aws_elasticloadbalancingv2


class LbListenerParameters:
    def __init__(
            self,
            production_listener: aws_elasticloadbalancingv2.CfnListener,
            production_listener_path: str,
            production_listener_rule_priority: int,
            deployment_listener: aws_elasticloadbalancingv2.CfnListener,
            deployment_listener_path: str,
            deployment_listener_rule_priority: int,
    ) -> None:
        """
        Constructor.

        :param production_listener: A loadbalancer's main production traffic listener instance.
        :param production_listener_path: A url path for a new deployed fargate service. For example "/fargate/*".
        :param production_listener_rule_priority: A priority of the rule to route traffic to the fargate service.
        :param deployment_listener: A loadbalancer's deployment/testing traffic listener instance.
        :param deployment_listener_path: A url path for a new deployed fargate service. For example "/fargate/*".
        :param deployment_listener_rule_priority: A priority of the rule to route traffic to the fargate service.

        :return: No return.
        """
        self.production_listener = production_listener
        self.production_listener_path = production_listener_path
        self.production_listener_rule_priority = production_listener_rule_priority

        self.deployment_listener = deployment_listener
        self.deployment_listener_path = deployment_listener_path
        self.deployment_listener_rule_priority = deployment_listener_rule_priority
