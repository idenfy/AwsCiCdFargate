from typing import Any, Dict, Optional
from aws_cdk import core
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_iam import Role, PolicyStatement, PolicyDocument, Effect, ServicePrincipal
from aws_cdk.custom_resources import AwsCustomResource, PhysicalResourceId


class DeploymentConfig:
    """
    Custom CloudFormation resource which creates a git commit action to set deployment configuration for ecs project.
    """
    def __init__(
            self,
            stack: core.Stack,
            prefix: str,
            code_repository: Repository,
            task_definition: str,
            app_spec: str
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
        self.__code_repository = code_repository
        self.__task_definition = task_definition
        self.__app_spec = app_spec

    def get_resource(self):
        """
        Creates a custom resource to manage an ecs deployment configuration.

        :param scope: A scope in which this resource should be created.

        :return: Custom resource to manage an ecs deployment configuration.
        """
        return AwsCustomResource(
            self.__stack,
            self.__prefix + "CustomDeploymentConfigResource",
            on_create=self.__on_create(),
            on_update=self.__on_update(),
            on_delete=self.__on_delete(),
            role=self.__role()
        )

    def __role(self) -> Role:
        """
        A role for custom resource which manages ecs deployment configuration.

        :return: Custom resource's role.
        """
        return Role(
            self.__stack,
            self.__prefix + 'FargateDeploymentConfigRole',
            inline_policies={
                self.__prefix + 'FargateDeploymentConfigPolicy': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            actions=[
                                "codecommit:CreateCommit",
                            ],
                            resources=[self.__code_repository.repository_arn],
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

    @staticmethod
    def service_name() -> str:
        """
        Returns a service name that this custom resource manages.

        :return: Service name.
        """
        return 'CodeCommit'

    def __on_create(self) -> Optional[Dict[Any, Any]]:
        """
        Creates an "on_create" command.

        :return: A dictionary command.
        """
        return {
            "service": self.service_name(),
            "action": "createCommit",
            "parameters": {
                'branchName': 'master',
                'repositoryName': self.__code_repository.repository_name,
                'commitMessage': 'Initial appspec and taskdef files.',
                'putFiles': [
                    {
                        'filePath': 'taskdef.json',
                        'fileMode': 'NORMAL',
                        'fileContent': self.__task_definition,
                    }, {
                        'filePath': 'appspec.yaml',
                        'fileMode': 'NORMAL',
                        'fileContent': self.__app_spec,
                    }
                ]
            },
            "physical_resource_id": PhysicalResourceId.of(self.__prefix + 'CreateCommit')
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
        return None
