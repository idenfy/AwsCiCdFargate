from typing import Union

from aws_cdk import core, aws_ecs, aws_codedeploy, aws_codecommit, aws_codebuild, aws_codepipeline, \
    aws_codepipeline_actions, aws_ecr, aws_ecs_patterns, aws_elasticloadbalancingv2, aws_ec2, aws_certificatemanager, aws_iam, aws_s3, aws_ec2
from aws_cdk.custom_resources import AwsCustomResource


class EcsPipeline:
    """
    Class which creates infrastructure for CI/CD Blue/Green Ecs Fargate deployment.
    """
    def __init__(
            self,
            prefix: str,
            aws_account_id: str,
            aws_region: str,
            main_target_group: aws_elasticloadbalancingv2.ApplicationTargetGroup,
            deployments_target_group: aws_elasticloadbalancingv2.ApplicationTargetGroup,
            main_listener: aws_elasticloadbalancingv2.ApplicationListener,
            deployments_listener: aws_elasticloadbalancingv2.ApplicationListener,
            ecs_service: aws_ecs.FargateService,
            ecs_cluster: aws_ecs.Cluster,
            artifact_builds_s3: aws_s3.Bucket,
            task_def: str,
            app_spec: str,
    ):
        """
        Constructor.
        :param prefix: A prefix for newly created resources.
        :param aws_account_id: An account id under which a CF stack is running.
        :param aws_region: Region in which the CF stack is running.
        :param main_target_group: A target group to which a loadbalancer is forwarding a received production traffic.
        :param deployments_target_group: A target group to which a loadbalancer is forwarding a received test traffic.
        :param main_listener: A listener which receives incoming traffic and forwards it to a target group.
        :param deployments_listener: A listener which receives incoming traffic and forwards it to a target group.
        This listener is used for blue/green deployment.
        :param ecs_service: Ecs service to which create this pipeline.
        :param ecs_cluster: ECS cluster in which the ECS service is.
        :param artifact_builds_s3: A S3 bucket to which built artifacts are written.
        :param task_def: Task definition object defining the parameters for a newly deployed container.
        :param app_spec: App specification object defining the ecs service modifications.
        """

        self.assume_principal = aws_iam.CompositePrincipal([
            aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
            aws_iam.ServicePrincipal('codedeploy.amazonaws.com')
        ])

        self.deployment_group_role = aws_iam.Role(
            self, 'deploymentRole',
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
            self, prefix + 'FargateEcsGitRepository',
            description='Repository containing appspec and taskdef files for ecs code-deploy blue/green deployments.',
            repository_name=prefix.lower() + '_config'
        )

        AwsCustomResource(self, prefix + 'FargateEcsDeploymentConfig',
                          on_create={
                              "service": "CodeCommit",
                              "action": "createCommit",
                              "parameters": {
                                  'BranchName': 'master',
                                  'commitMessage': 'Initial appspec and taskdef files.',
                                  'putFiles': [
                                      {
                                          'filePath': 'taskdef.json',
                                          'fileMode': 'NORMAL',
                                          'fileContent': task_def,
                                      }, {
                                          'filePath': 'appspec.yaml',
                                          'fileMode': 'NORMAL',
                                          'fileContent': app_spec,
                                      }
                                  ]
                              },
                          },
                          )
        self.ecr_repository = aws_ecr.Repository(
            self, prefix + 'FargateEcsEcrRepository',
            repository_name=prefix.lower()
        )

        self.ecr_repository_output_artifact = aws_codepipeline.Artifact('EcsImage')
        self.config_output_artifact = aws_codepipeline.Artifact('EcsConfig')

        self.application = aws_codedeploy.EcsApplication(
            self, prefix + 'FargateEcsCodeDeployApplication',
            application_name=prefix + 'FargateEcsCodeDeployApplication',
        )

        AwsCustomResource(self, prefix + 'FargateEcsDeploymentGroup',
                          on_create={
                              "service": "CodeDeploy",
                              "action": "createDeploymentGroup",
                              "parameters": {
                                  'applicationName': self.application.ApplicationName,
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
                                                      'name': main_target_group.target_group_name
                                                  },
                                                  {
                                                      'name': deployments_target_group.target_group_name
                                                  },
                                              ],
                                              'prodTrafficRoute': {
                                                  'listenerArns': [
                                                      main_listener.listener_arn
                                                  ]
                                              },
                                              'testTrafficRoute': {
                                                  'listenerArns': [
                                                      main_listener.listener_arn
                                                  ]
                                              }
                                          },
                                      ]
                                  },
                                  'ecsServices': [
                                      {
                                          'serviceName': ecs_service.service_name,
                                          'clusterName': ecs_cluster.cluster_name
                                      },
                                  ],
                              },
                          },
                          )
        self.deployment_group = aws_codedeploy.EcsDeploymentGroup.from_ecs_deployment_group_attributes(
            self, prefix + 'FargateEcsDeploymentGroup',
            application=self.application,
            deployment_group_name=prefix + 'FargateEcsDeploymentGroup',
        )

        self.pipeline = aws_codepipeline.Pipeline(
            self, prefix + 'FargateEcsPipeline',
            artifact_bucket=artifact_builds_s3,
            pipeline_name=prefix + 'FargateEcsPipeline',
            stages=[
                aws_codepipeline.StageProps(
                    stage_name='SourceStage',
                    actions=[
                        aws_codepipeline_actions.EcrSourceAction(
                            action_name='SourceEcrAction',
                            output=self.ecr_repository_output_artifact,
                            image_tag=f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com/{self.ecr_repository.repository_uri}:latest',
                            repository=self.ecr_repository,
                            run_order=1
                        ),
                        aws_codepipeline_actions.CodeCommitSourceAction(
                            action_name='SourceCodeCommitAction',
                            output=self.config_output_artifact,
                            repository=self.git_repository,
                            branch='master',
                            run_order=1
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
                            container_image_inputs=aws_codepipeline_actions.CodeDeployEcsContainerImageInput(
                                input=self.ecr_repository_output_artifact,
                                task_definition_placeholder='IMAGE1_NAME'
                            ),
                            run_order=1
                        )
                    ]
                )
            ]
        )

