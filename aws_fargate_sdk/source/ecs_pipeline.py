import json
import re

from aws_cdk.custom_resources import AwsCustomResource
from aws_empty_bucket.empty_s3_bucket import EmptyS3Bucket
from aws_cdk import (
    aws_ecs,
    aws_codedeploy,
    aws_codecommit,
    aws_codepipeline,
    aws_codepipeline_actions,
    aws_ecr,
    aws_elasticloadbalancingv2,
    aws_iam,
    aws_s3,
    aws_codebuild,
    core
)


class EcsPipeline:
    """
    Class which creates infrastructure for CI/CD Blue/Green Ecs Fargate deployment.
    """

    def __init__(
            self,
            scope: core.Stack,
            prefix: str,
            aws_region: str,
            main_listener: aws_elasticloadbalancingv2.CfnListener,
            deployments_listener: aws_elasticloadbalancingv2.CfnListener,
            ecs_service: AwsCustomResource,
            ecs_cluster: aws_ecs.Cluster,
            task_def: str,
            app_spec: str,
    ):
        """
        Constructor.
        :param prefix: A prefix for newly created resources.
        :param aws_region: Region in which the CF stack is running.
        :param main_listener: A listener which receives incoming traffic and forwards it to a target group.
        :param deployments_listener: A listener which receives incoming traffic and forwards it to a target group.
        This listener is used for blue/green deployment.
        :param ecs_service: Ecs service to which create this pipeline.
        :param ecs_cluster: ECS cluster in which the ECS service is.
        :param task_def: Task definition object defining the parameters for a newly deployed container.
        :param app_spec: App specification object defining the ecs service modifications.
        """
        self.artifacts_bucket = EmptyS3Bucket(
            scope,
            self.__convert(prefix + 'ArtifactsBucket'),
            access_control=aws_s3.BucketAccessControl.PRIVATE,
            bucket_name=self.__convert(prefix + 'ArtifactsBucket'),
        )

        self.assume_principal = aws_iam.CompositePrincipal(
            aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
            aws_iam.ServicePrincipal('codedeploy.amazonaws.com')
        )

        self.deployment_group_role = aws_iam.Role(
            scope, prefix + 'FargateEcsDeploymentGroupRole',
            path='/',
            inline_policies={'firstpolicy': aws_iam.PolicyDocument(
                statements=[aws_iam.PolicyStatement(
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
                    effect=aws_iam.Effect.ALLOW)]
            )},
            assumed_by=self.assume_principal
        )

        self.git_repository = aws_codecommit.Repository(
            scope, prefix + 'FargateEcsGitRepository',
            description='Repository containing appspec and taskdef files for ecs code-deploy blue/green deployments.',
            repository_name=prefix.lower() + '-config'
        )

        self.commit_custom = AwsCustomResource(
            scope, prefix + 'FargateEcsDeploymentConfig',
            on_create={
                "service": "CodeCommit",
                "action": "createCommit",
                "parameters": {
                    'branchName': 'master',
                    'repositoryName': self.git_repository.repository_name,
                    'commitMessage': 'Initial appspec and taskdef files.',
                    'putFiles': [
                        {
                            'filePath': 'taskdef.json',
                            'fileMode': 'NORMAL',
                            'fileContent': json.dumps(task_def, indent=4),
                        }, {
                            'filePath': 'appspec.yaml',
                            'fileMode': 'NORMAL',
                            'fileContent': app_spec,
                        }
                    ]
                },
                "physical_resource_id": '123',
            },
        )

        self.ecr_repository = aws_ecr.Repository(
            scope, prefix + 'FargateEcsEcrRepository',
            repository_name=prefix.lower()
        )

        self.ecr_repository_output_artifact = aws_codepipeline.Artifact('EcsImage')
        self.config_output_artifact = aws_codepipeline.Artifact('EcsConfig')

        self.application = aws_codedeploy.EcsApplication(
            scope, prefix + 'FargateEcsCodeDeployApplication',
            application_name=prefix + 'FargateEcsCodeDeployApplication',
        )

        self.deployment_group_custom = AwsCustomResource(
            scope, prefix + 'FargateEcsDeploymentGroup',
            on_create={
                "service": "CodeDeploy",
                "action": "createDeploymentGroup",
                "parameters": {
                    'applicationName': self.application.application_name,
                    'deploymentGroupName': prefix + 'FargateEcsDeploymentGroup',
                    'deploymentConfigName': 'CodeDeployDefault.ECSAllAtOnce',
                    'serviceRoleArn': self.deployment_group_role.role_arn,
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
                                        'name': prefix + 'FargateEcsTargetGroup1',
                                    },
                                    {
                                        'name': prefix + 'FargateEcsTargetGroup2',
                                    },
                                ],
                                'prodTrafficRoute': {
                                    'listenerArns': [
                                        main_listener.ref
                                    ]
                                },
                                'testTrafficRoute': {
                                    'listenerArns': [
                                        deployments_listener.ref
                                    ]
                                }
                            },
                        ]
                    },
                    'ecsServices': [
                        {
                            'serviceName': prefix + 'FargateEcsService',
                            'clusterName': ecs_cluster.cluster_name
                        },
                    ],
                },
                'physical_resource_id': '456'
            },
            on_update={
                "service": "CodeDeploy",
                "action": "updateDeploymentGroup",
                "parameters": {
                    'applicationName': self.application.application_name,
                    'deploymentGroupName': prefix + 'FargateEcsDeploymentGroup',
                    'deploymentConfigName': 'CodeDeployDefault.ECSAllAtOnce',
                    'serviceRoleArn': self.deployment_group_role.role_arn,
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
                                        'name': prefix + 'FargateEcsTargetGroup1',
                                    },
                                    {
                                        'name': prefix + 'FargateEcsTargetGroup2',
                                    },
                                ],
                                'prodTrafficRoute': {
                                    'listenerArns': [
                                        main_listener.ref
                                    ]
                                },
                                'testTrafficRoute': {
                                    'listenerArns': [
                                        deployments_listener.ref
                                    ]
                                }
                            },
                        ]
                    },
                    'ecsServices': [
                        {
                            'serviceName': prefix + 'FargateEcsService',
                            'clusterName': ecs_cluster.cluster_name
                        },
                    ],
                },
                'physical_resource_id': '456'
            },
            on_delete={
                'physical_resource_id': '456',
                "service": "CodeDeploy",
                "action": "deleteDeploymentGroup",
                "parameters": {
                    'applicationName': self.application.application_name,
                    'deploymentGroupName': prefix + 'FargateEcsDeploymentGroup',
                }
            }
        )

        self.deployment_group_custom.node.add_dependency(ecs_service)
        self.deployment_group_custom.node.add_dependency(ecs_cluster)
        self.deployment_group = aws_codedeploy.EcsDeploymentGroup.from_ecs_deployment_group_attributes(
            scope, prefix + 'FargateEcsDeploymentGroupReal',
            application=self.application,
            deployment_group_name=prefix + 'FargateEcsDeploymentGroup',
        )

        self.deployment_group.node.add_dependency(self.deployment_group_custom)

        self.pipeline = aws_codepipeline.Pipeline(
            scope, prefix + 'FargateEcsPipeline',
            artifact_bucket=self.artifacts_bucket,
            pipeline_name=prefix + 'FargateEcsEcrPipeline',
            stages=[
                aws_codepipeline.StageProps(
                    stage_name='SourceStage',
                    actions=[
                        aws_codepipeline_actions.EcrSourceAction(
                            action_name='SourceEcrAction',
                            output=self.ecr_repository_output_artifact,
                            repository=self.ecr_repository,
                            run_order=1,
                        ),
                        aws_codepipeline_actions.CodeCommitSourceAction(
                            action_name='SourceCodeCommitAction',
                            output=self.config_output_artifact,
                            repository=self.git_repository,
                            branch='master',
                            run_order=1,
                        )
                    ]
                ),
                aws_codepipeline.StageProps(
                    stage_name='DeployStage',
                    actions=[
                        aws_codepipeline_actions.CodeDeployEcsDeployAction(
                            action_name='DeployAction',
                            deployment_group=self.deployment_group,
                            app_spec_template_input=self.config_output_artifact,
                            task_definition_template_input=self.config_output_artifact,
                            container_image_inputs=[
                                aws_codepipeline_actions.CodeDeployEcsContainerImageInput(
                                    input=self.ecr_repository_output_artifact,
                                    task_definition_placeholder='IMAGE1_NAME'
                                )
                            ],
                            run_order=1
                        )
                    ]
                )
            ]
        )

        self.pipeline.node.add_dependency(self.commit_custom)

        self.codecommit_repo = aws_codecommit.Repository(
            scope, prefix + 'FargateEcsCodeCommitSource',
            repository_name=prefix + 'FargateEcsCodeCommitSource'
        )

        self.source_artifact = aws_codepipeline.Artifact(
            artifact_name=prefix + 'FargateEcsCodeCommitSourceArtifact',
        )

        self.source_action = aws_codepipeline_actions.CodeCommitSourceAction(
            repository=self.codecommit_repo,
            branch='master',
            action_name='CodeCommitSource',
            run_order=1,
            trigger=aws_codepipeline_actions.CodeCommitTrigger.EVENTS,
            output=self.source_artifact
        )

        self.docker_build = aws_codebuild.PipelineProject(
            scope, prefix + 'FargateEcsCodeBuildProject',
            project_name=prefix + 'FargateEcsCodeBuildProject',
            environment_variables={
                'REPOSITORY_URI': aws_codebuild.BuildEnvironmentVariable(value=self.ecr_repository.repository_uri),
                'PIPELINE_NAME': aws_codebuild.BuildEnvironmentVariable(value=self.pipeline.pipeline_name),
                'REGION': aws_codebuild.BuildEnvironmentVariable(value=aws_region)
            },
            environment=aws_codebuild.BuildEnvironment(
                build_image=aws_codebuild.LinuxBuildImage.UBUNTU_14_04_DOCKER_18_09_0,
                compute_type=aws_codebuild.ComputeType.SMALL,
                privileged=True
            ),
            build_spec=aws_codebuild.BuildSpec.from_object(
                {
                    'version': 0.2,
                    'phases': {
                        'pre_build': {
                            'commands': f'$(aws ecr get-login --no-include-email --region $REGION)'
                        },
                        'build': {
                            'commands': 'docker build -t $REPOSITORY_URI:latest .',
                        },
                        'post_build': {
                            'commands': [
                                'docker push $REPOSITORY_URI:latest',
                                f'aws codepipeline start-pipeline-execution --name $PIPELINE_NAME'
                            ]
                        },
                    }
                }
            ),

        )

        self.docker_build.role.add_to_policy(
            statement=aws_iam.PolicyStatement(
                actions=[
                    "ecr:CompleteLayerUpload",
                    "ecr:GetAuthorizationToken",
                    "ecr:UploadLayerPart",
                    "ecr:InitiateLayerUpload",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:PutImage",
                    "codepipeline:StartPipelineExecution"
                ],
                resources=['*'],
                effect=aws_iam.Effect.ALLOW)
        )

        self.second_pipieline = aws_codepipeline.Pipeline(
            scope, prefix + 'FargateEcsFirstPipeline',
            pipeline_name=prefix + 'FargateEcsCommitPipeline',
            artifact_bucket=self.artifacts_bucket,
            stages=[
                aws_codepipeline.StageProps(
                    stage_name='SourceStage',
                    actions=[self.source_action]
                ),
                aws_codepipeline.StageProps(
                    stage_name='BuildStage',
                    actions=[
                        aws_codepipeline_actions.CodeBuildAction(
                            input=self.source_artifact,
                            project=self.docker_build,
                            action_name='BuildAction',
                            run_order=1
                        )
                    ]
                )
            ]
        )
    @staticmethod
    def __convert(name: str) -> str:
        """
        Converts CamelCase string to pascal-case where underscores are dashes.
        This is required due to S3 not supporting capital letters or underscores.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
