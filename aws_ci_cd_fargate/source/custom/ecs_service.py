from typing import Any, Dict, Optional
from aws_cdk import core, aws_ecs
from aws_cdk.aws_elasticloadbalancingv2 import CfnTargetGroup
from aws_ci_cd_fargate.parameters.ecs_parameters import EcsParams
from aws_ecs_service.ecs_service import EcsService as EcsServiceCustomResource


class EcsService:
    """
    Custom CloudFormation resource which creates a git commit action to set deployment configuration for ecs project.
    """

    def __init__(
            self,
            stack: core.Stack,
            prefix: str,
            cluster: aws_ecs.Cluster,
            task: aws_ecs.FargateTaskDefinition,
            ecs_params: EcsParams,
            production_target_group: CfnTargetGroup
    ) -> None:
        """
        Constructor.

        :param stack: A CloudFormation stack to which add this resource.
        :param prefix: Prefix for resource names.
        :param code_repository: A codecommit git repository to push configuration files for ecs deployment.
        :param task_definition: A document which describes how ecs deployment should behave.
        :param app_spec: A document which describes how ecs deployment should behave.
        """
        self.__stack = stack
        self.__prefix = prefix
        self.__cluster = cluster
        self.__task = task
        self.__ecs_params = ecs_params
        self.__production_target_group = production_target_group

    def get_resource(self) -> EcsServiceCustomResource:
        """
        Creates a custom resource to manage an ecs deployment configuration.

        :param scope: A scope in which this resource should be created.

        :return: Custom resource to manage an ecs deployment configuration.
        """
        return EcsServiceCustomResource(
            scope=self.__stack,
            id=self.__prefix + "FargateService",
            on_create_action=self.__on_create(),
            on_update_action=self.__on_update(),
            on_delete_action=self.__on_delete()
        )

    def __on_create(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_create" command.

        :return: A dictionary command.
        """
        return {
            'cluster': self.__cluster.cluster_arn,
            'serviceName': self.__prefix + 'FargateService',
            'taskDefinition': self.__task.task_definition_arn,
            'loadBalancers': [
                {
                    'containerName': self.__ecs_params.container_name,
                    'containerPort': 80,
                    'targetGroupArn': self.__production_target_group.ref
                }
            ],
            'desiredCount': 1,
            'networkConfiguration': {
                'awsvpcConfiguration': {
                    'assignPublicIp': 'DISABLED',
                    'securityGroups': [sub.security_group_id for sub in self.__ecs_params.ecs_security_groups],
                    'subnets': [sub.subnet_id for sub in self.__ecs_params.ecs_subnets],
                }
            },
            'deploymentController': {
                'type': 'CODE_DEPLOY'
            },
            'launchType': 'FARGATE'
        }

    def __on_update(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_update" command".

        :return: A dictionary command.
        """
        return {
            'cluster': self.__cluster.cluster_arn,
            'service': self.__prefix + 'FargateService',
            'healthCheckGracePeriodSeconds': 0
        }

    def __on_delete(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_delete" command".

        :return: A dictionary command.
        """
        return {
            'cluster': self.__cluster.cluster_arn,
            'service': self.__prefix + 'FargateService',
            'force': True
        }
