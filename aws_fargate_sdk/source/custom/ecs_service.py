from typing import Any, Dict, Optional
from aws_cdk import core, aws_ecs
from aws_cdk.aws_elasticloadbalancingv2 import CfnTargetGroup
from aws_cdk.custom_resources import AwsCustomResource
from aws_fargate_sdk.parameters.ecs_parameters import EcsParams


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

    def get_resource(self):
        """
        Creates a custom resource to manage an ecs deployment configuration.

        :param scope: A scope in which this resource should be created.

        :return: Custom resource to manage an ecs deployment configuration.
        """
        return AwsCustomResource(
            self.__stack,
            self.__prefix + "FargateService",
            on_create=self.__on_create(),
            on_update=self.__on_update(),
            on_delete=self.__on_delete()
        )

    @staticmethod
    def service_name() -> str:
        """
        Returns a service name that this custom resource manages.

        :return: Service name.
        """
        return 'ECS'

    def __on_create(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_create" command.

        :return: A dictionary command.
        """
        return {
            "service": self.service_name(),
            "action": 'createService',
            "physical_resource_id": self.__prefix + 'FargateServiceCustom',
            'parameters': {
                'cluster': self.__cluster.cluster_arn,
                'serviceName': self.__prefix + 'FargateService',
                'taskDefinition': self.__task.task_definition_arn,
                'loadBalancers': [
                    {
                        'containerName': self.__ecs_params.container_name,
                        'containerPort': self.__ecs_params.container_port,
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
        }

    def __on_update(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_update" command".

        :return: A dictionary command.
        """
        return None

    def __on_delete(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_delete" command".

        :return: A dictionary command.
        """
        return {
            "service": self.service_name(),
            "action": 'deleteService',
            "physical_resource_id": self.__prefix + 'FargateServiceCustom',
            'parameters': {
                'cluster': self.__cluster.cluster_arn,
                'service': self.__prefix + 'FargateService',
                'force': True
            }
        }
