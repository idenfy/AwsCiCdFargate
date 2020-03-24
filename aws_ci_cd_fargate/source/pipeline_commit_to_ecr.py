import copy

from typing import Dict, Any
from aws_cdk import aws_codepipeline, aws_codepipeline_actions, aws_codecommit, aws_iam, aws_codebuild, aws_ecr
from aws_cdk.aws_codepipeline import IPipeline
from aws_cdk.aws_s3 import IBucket
from aws_cdk.core import Stack


class PipelineCommitToEcr:
    def __init__(
            self,
            scope: Stack,
            prefix: str,
            artifacts_bucket: IBucket,
            ecr_repository: aws_ecr.Repository,
            source_repository: aws_codecommit.Repository,
            build_environment: Dict[str, Any],
            docker_build_args: Dict[str, str],
            next_pipeline: IPipeline
    ):
        self.region = scope.region
        self.ecr_repository = ecr_repository
        self.build_environment = build_environment
        self.next_pipeline = next_pipeline

        self.source_artifact = aws_codepipeline.Artifact(
            artifact_name=prefix + 'FargateCodeCommitSourceArtifact',
        )

        self.source_action = aws_codepipeline_actions.CodeCommitSourceAction(
            repository=source_repository,
            branch='master',
            action_name='CodeCommitSource',
            run_order=1,
            trigger=aws_codepipeline_actions.CodeCommitTrigger.EVENTS,
            output=self.source_artifact
        )

        docker_build_command = 'docker build -t $REPOSITORY_URI:latest .'

        for key, value in docker_build_args.items():
            docker_build_command += f' --build-arg {key}={value}'

        self.docker_build = aws_codebuild.PipelineProject(
            scope, prefix + 'FargateCodeBuildProject',
            project_name=prefix + 'FargateCodeBuildProject',
            environment_variables=self.build_environment_variables(),
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
                            'commands': docker_build_command,
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

        self.codecommit_to_ecr_pipeline = aws_codepipeline.Pipeline(
            scope,
            prefix + 'FargateCodeCommitToEcrPipeline',
            pipeline_name=prefix + 'FargateCodeCommitToEcrPipeline',
            artifact_bucket=artifacts_bucket,
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

    def build_environment_variables(self):
        base_environment = {
            'REPOSITORY_URI': aws_codebuild.BuildEnvironmentVariable(value=self.ecr_repository.repository_uri),
            'PIPELINE_NAME': aws_codebuild.BuildEnvironmentVariable(value=self.next_pipeline.pipeline_name),
            'REGION': aws_codebuild.BuildEnvironmentVariable(value=self.region)
        }

        build_environment = copy.deepcopy(self.build_environment)
        build_environment.pop('REPOSITORY_URI', None)
        build_environment.pop('PIPELINE_NAME', None)
        build_environment.pop('REGION', None)

        for key, value in build_environment.items():
            if not isinstance(value, aws_codebuild.BuildEnvironmentVariable):
                build_environment[key] = aws_codebuild.BuildEnvironmentVariable(value=value)

        return {**base_environment, **build_environment}
