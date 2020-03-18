from aws_cdk import aws_elasticloadbalancingv2


class LbListenerParameters:
    def __init__(
            self,
            production_listener: aws_elasticloadbalancingv2.CfnListener,
            deployment_listener: aws_elasticloadbalancingv2.CfnListener,
            rule_condition: aws_elasticloadbalancingv2.CfnListenerRule.RuleConditionProperty,
            rule_priority: int,
    ) -> None:
        """
        Constructor.

        :param production_listener: A loadbalancer's main (blue) listener instance.
        :param deployment_listener: A loadbalancer's test (green) traffic listener instance.
        :param rule_condition: A listener routing rule condition. When a rule is matched, the
        traffic is picked up by the listeners and sent to target groups. Read more:
        https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-update-rules.html
        :param rule_priority: A priority for the rule. The lower the number, the higher the priority.
        Read more: https://stackoverflow.com/questions/43385942/aws-alb-rule-priority

        :return: No return.
        """
        self.production_listener = production_listener
        self.deployment_listener = deployment_listener
        self.rule_condition = rule_condition
        self.rule_priority = rule_priority
