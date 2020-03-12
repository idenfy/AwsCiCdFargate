from typing import Any, Dict, Optional
from aws_cdk import core
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codedeploy import EcsApplication
from aws_cdk.aws_ecs import Cluster
from aws_cdk.aws_elasticloadbalancingv2 import CfnListener
from aws_cdk.aws_iam import Role, PolicyStatement, PolicyDocument, Effect, ServicePrincipal, CompositePrincipal
from aws_cdk.custom_resources import AwsCustomResource, PhysicalResourceId


class DeploymentGroup:
    """
    Custom CloudFormation resource which manages a deployment group.
    """
    def __init__(
            self,
            stack: core.Stack,
            prefix: str,
            code_repository: Repository,
            task_definition: str,
            app_spec: str,
            ecs_application: EcsApplication,
            main_listener: CfnListener,
            deployments_listener: CfnListener,
            production_target_group,
            deployment_target_group,
            ecs_cluster: Cluster,
    ) -> None:
        """
        Constructor.

        :param stack: A CloudFormation stack to which add this resource.
        :param prefix: Prefix for resource names.
        :param code_repository: A codecommit git repository to push configuration files for ecs deployment.
        :param task_definition: A document which describes how ecs deployment should behave.
        :param app_spec: A document which describes how ecs deployment should behave.
        :param ecs_application: An ecs application for which the deployments are being made.
        :param main_listener: A loadbalancer's main listener for main traffic.
        :param deployments_listener: A loadbalancer's testing listener for testing traffic.
        :param ecs_cluster: An ecs cluster in which our ecs application is located.
        """
        self.__stack = stack
        self.__prefix = prefix
        self.__code_repository = code_repository
        self.__task_definition = task_definition
        self.__app_spec = app_spec
        self.__ecs_application = ecs_application
        self.__main_listener = main_listener
        self.__deployments_listener = deployments_listener
        self.__production_target_group = production_target_group
        self.__deployment_target_group = deployment_target_group
        self.__ecs_cluster = ecs_cluster

        self.__custom_resource_role = Role(
            self.__stack,
            self.__prefix + 'CustomFargateDeploymentGroupRole',
            inline_policies={
                self.__prefix + 'CustomFargateDeploymentGroupPolicy': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                "codedeploy:GetDeploymentGroup",
                                "codedeploy:CreateDeploymentGroup",
                                "codedeploy:DeleteDeploymentGroup",
                                "codedeploy:UpdateDeploymentGroup",
                            ],
                            resources=['*'],
                            effect=Effect.ALLOW
                        ),
                        PolicyStatement(
                            actions=[
                                "logs:CreateLogGroup",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents"
                            ],
                            resources=['*'],
                            effect=Effect.ALLOW
                        )
                    ]
                )},
            assumed_by=ServicePrincipal('lambda.amazonaws.com')
        )

        self.__deployment_group_role = Role(
            self.__stack,
            self.__prefix + 'FargateDeploymentGroupRole',
            path='/',
            inline_policies={
                self.__prefix + 'FargateDeploymentGroupPolicy': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                "ecs:DescribeServices",
                                "ecs:CreateTaskSet",
                                "ecs:UpdateServicePrimaryTaskSet",
                                "ecs:DeleteTaskSet",
                                "elasticloadbalancing:DescribeTargetGroups",
                                "elasticloadbalancing:DescribeListeners",
                                "elasticloadbalancing:ModifyListener",
                                "elasticloadbalancing:DescribeRules",
                                "elasticloadbalancing:ModifyRule",
                                "lambda:InvokeFunction",
                                "cloudwatch:DescribeAlarms",
                                "sns:Publish",
                                "s3:GetObject",
                                "s3:GetObjectMetadata",
                                "s3:GetObjectVersion",
                                "iam:PassRole"
                            ],
                            resources=['*'],
                            effect=Effect.ALLOW
                        )
                    ]
                )
            },
            assumed_by=CompositePrincipal(
                ServicePrincipal('ecs-tasks.amazonaws.com'),
                ServicePrincipal('codedeploy.amazonaws.com')
            )
        )

    def get_resource(self):
        """
        Creates a custom resource to manage a deployment group.

        :return: Custom resource to manage a deployment group.
        """
        return AwsCustomResource(
            scope=self.__stack,
            id=self.__prefix + "CustomFargateDeploymentGroupResource",
            on_create=self.__on_create(),
            on_update=self.__on_update(),
            on_delete=self.__on_delete(),
            role=self.__custom_resource_role
        )

    @staticmethod
    def service_name() -> str:
        """
        Returns a service name that this custom resource manages.

        :return: Service name.
        """
        return 'CodeDeploy'

    def __on_create(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_create" command.

        :return: A dictionary command.
        """
        return {
            "service": self.service_name(),
            "action": "createDeploymentGroup",
            "parameters": {
                'applicationName': self.__ecs_application.application_name,
                'deploymentGroupName': self.__prefix + 'FargateDeploymentGroup',
                'deploymentConfigName': 'CodeDeployDefault.ECSAllAtOnce',
                'serviceRoleArn': self.__deployment_group_role.role_arn,
                'autoRollbackConfiguration': {
                    'enabled': True,
                    'events': ['DEPLOYMENT_FAILURE', 'DEPLOYMENT_STOP_ON_ALARM', 'DEPLOYMENT_STOP_ON_REQUEST']
                },
                'deploymentStyle': {
                    'deploymentType': 'BLUE_GREEN',
                    'deploymentOption': 'WITH_TRAFFIC_CONTROL'
                },
                'blueGreenDeploymentConfiguration': {
                    'terminateBlueInstancesOnDeploymentSuccess': {
                        'action': 'TERMINATE',
                        'terminationWaitTimeInMinutes': 5
                    },
                    'deploymentReadyOption': {
                        'actionOnTimeout': 'CONTINUE_DEPLOYMENT',
                    },
                },
                'loadBalancerInfo': {
                    'targetGroupPairInfoList': [
                        {
                            'targetGroups': [
                                {
                                    'name': self.__production_target_group.attr_target_group_name,
                                },
                                {
                                    'name': self.__deployment_target_group.attr_target_group_name,
                                },
                            ],
                            'prodTrafficRoute': {
                                'listenerArns': [
                                    self.__main_listener.ref
                                ]
                            },
                            'testTrafficRoute': {
                                'listenerArns': [
                                    self.__deployments_listener.ref
                                ]
                            }
                        },
                    ]
                },
                'ecsServices': [
                    {
                        'serviceName': self.__prefix + 'FargateService',
                        'clusterName': self.__ecs_cluster.cluster_name
                    },
                ],
            },
            "physical_resource_id": PhysicalResourceId.of(self.__prefix + 'DeploymentGroup'),
        }

    def __on_update(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_update" command".

        :return: A dictionary command.
        """
        return {
            "service": self.service_name(),
            "action": "updateDeploymentGroup",
            "parameters": {
                'applicationName': self.__ecs_application.application_name,
                'currentDeploymentGroupName': self.__prefix + 'FargateDeploymentGroup',
                'deploymentConfigName': 'CodeDeployDefault.ECSAllAtOnce',
                'serviceRoleArn': self.__deployment_group_role.role_arn,
                'autoRollbackConfiguration': {
                    'enabled': True,
                    'events': ['DEPLOYMENT_FAILURE', 'DEPLOYMENT_STOP_ON_ALARM', 'DEPLOYMENT_STOP_ON_REQUEST']
                },
                'deploymentStyle': {
                    'deploymentType': 'BLUE_GREEN',
                    'deploymentOption': 'WITH_TRAFFIC_CONTROL'
                },
                'blueGreenDeploymentConfiguration': {
                    'terminateBlueInstancesOnDeploymentSuccess': {
                        'action': 'TERMINATE',
                        'terminationWaitTimeInMinutes': 5
                    },
                    'deploymentReadyOption': {
                        'actionOnTimeout': 'CONTINUE_DEPLOYMENT',
                    },
                },
                'loadBalancerInfo': {
                    'targetGroupPairInfoList': [
                        {
                            'targetGroups': [
                                {
                                    'name': self.__production_target_group.attr_target_group_name,
                                },
                                {
                                    'name': self.__deployment_target_group.attr_target_group_name,
                                },
                            ],
                            'prodTrafficRoute': {
                                'listenerArns': [
                                    self.__main_listener.ref
                                ]
                            },
                            'testTrafficRoute': {
                                'listenerArns': [
                                    self.__deployments_listener.ref
                                ]
                            }
                        },
                    ]
                },
                'ecsServices': [
                    {
                        'serviceName': self.__prefix + 'FargateService',
                        'clusterName': self.__ecs_cluster.cluster_name
                    },
                ],
            },
            "physical_resource_id": PhysicalResourceId.of(self.__prefix + 'DeploymentGroup'),
        }

    def __on_delete(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_delete" command".

        :return: A dictionary command.
        """


        return {
            "service": self.service_name(),
            "action": "deleteDeploymentGroup",
            "parameters": {
                'applicationName': self.__ecs_application.application_name,
                'deploymentGroupName': self.__prefix + 'FargateDeploymentGroup',
            },
            "physical_resource_id": PhysicalResourceId.of(self.__prefix + 'DeploymentGroup'),
        }
