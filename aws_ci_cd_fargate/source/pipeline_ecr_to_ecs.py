from aws_cdk import aws_codepipeline, aws_codepipeline_actions, aws_codecommit, aws_codedeploy, aws_elasticloadbalancingv2, aws_ecs, aws_ecr
from aws_cdk.aws_ecs import CfnService
from aws_cdk.aws_s3 import IBucket
from aws_cdk.core import Stack
from aws_ci_cd_fargate.source.custom.deployment_config import DeploymentConfig
from aws_ci_cd_fargate.source.custom.deployment_group import DeploymentGroup


class PipelineEcrToEcs:
    def __init__(
            self,
            scope: Stack,
            prefix: str,
            artifacts_bucket: IBucket,
            source_repository: aws_codecommit.Repository,
            ecr_repository: aws_ecr.Repository,
            task_def: str,
            app_spec: str,
            main_listener: aws_elasticloadbalancingv2.CfnListener,
            deployments_listener: aws_elasticloadbalancingv2.CfnListener,
            ecs_cluster: aws_ecs.Cluster,
            ecs_service: CfnService,
            production_target_group,
            deployment_target_group
    ):
        self.application = aws_codedeploy.EcsApplication(
            scope, prefix + 'FargateCodeDeployApplication',
            application_name=prefix + 'FargateCodeDeployApplication',
        )

        self.deployment_group_custom = DeploymentGroup(
            stack=scope,
            prefix=prefix,
            code_repository=source_repository,
            task_definition=task_def,
            app_spec=app_spec,
            ecs_application=self.application,
            main_listener=main_listener,
            deployments_listener=deployments_listener,
            ecs_cluster=ecs_cluster,
            production_target_group=production_target_group,
            deployment_target_group=deployment_target_group
        ).get_resource()

        self.deployment_group_custom.node.add_dependency(ecs_service)
        self.deployment_group_custom.node.add_dependency(ecs_cluster)

        self.deployment_group = aws_codedeploy.EcsDeploymentGroup.from_ecs_deployment_group_attributes(
            scope, prefix + 'FargateDeploymentGroup',
            application=self.application,
            deployment_group_name=prefix + 'FargateDeploymentGroup',
        )

        self.deployment_group.node.add_dependency(self.deployment_group_custom)

        self.deployment_config_repository = aws_codecommit.Repository(
            scope, prefix + 'FargateDeploymentConfigRepository',
            description='Repository containing appspec and taskdef files for ecs code-deploy blue/green deployments.',
            repository_name=prefix.lower() + '-deployment-config'
        )

        self.commit_custom = DeploymentConfig(
            stack=scope,
            prefix=prefix,
            code_repository=self.deployment_config_repository,
            task_definition=task_def,
            app_spec=app_spec
        ).get_resource()

        self.ecr_repository_output_artifact = aws_codepipeline.Artifact('EcsImage')
        self.config_output_artifact = aws_codepipeline.Artifact('EcsConfig')

        self.ecr_to_ecs_pipeline = aws_codepipeline.Pipeline(
            scope,
            prefix + 'FargateEcrToEcsPipeline',
            artifact_bucket=artifacts_bucket,
            pipeline_name=prefix + 'FargateEcrToEcsPipeline',
            stages=[
                aws_codepipeline.StageProps(
                    stage_name='SourceStage',
                    actions=[
                        aws_codepipeline_actions.EcrSourceAction(
                            action_name='SourceEcrAction',
                            output=self.ecr_repository_output_artifact,
                            repository=ecr_repository,
                            run_order=1,
                        ),
                        aws_codepipeline_actions.CodeCommitSourceAction(
                            action_name='SourceCodeCommitAction',
                            output=self.config_output_artifact,
                            repository=self.deployment_config_repository,
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

        self.ecr_to_ecs_pipeline.node.add_dependency(self.commit_custom)
