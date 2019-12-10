from typing import List, Dict, Optional

from aws_cdk import core, aws_ecs, aws_codedeploy, aws_codecommit, aws_codebuild, aws_codepipeline, \
    aws_codepipeline_actions, aws_ecr, aws_ecs_patterns, aws_elasticloadbalancingv2, aws_ec2, aws_certificatemanager, aws_iam, aws_s3, aws_ec2
from aws_cdk.custom_resources import AwsCustomResource

from hello_cdk.ecs_autoscaling import Autoscaling
from hello_cdk.ecs_autoscaling import Autoscaling
from hello_cdk.ecs_loadbalancer import Loadbalancing
from hello_cdk.ecs_main import Ecs
from hello_cdk.ecs_pipeline import EcsPipeline

class EcsParams:
    """
    Parameters class which specifies deployed container and ecs parameters such as name, port, etc.
    """
    def __init__(
            self,
            container_name: str,
            container_cpu: str,
            container_ram: str,
            container_port: int,
            container_environment: Dict[str, any],
            ecs_security_groups: List[aws_ec2.SecurityGroup],
            ecs_subnets: List[aws_ec2.Subnet]
    ) -> None:
        """
        Constructor.
        :param container_name: The name that will be given to a newly deployed container.
        :param container_cpu: Cpu points for the deployed container. 1 CPU = 1024 Cpu units.
        :param container_ram: Memory for the deployed container. 1 GB Ram = 1024 units.
        :param container_port: An open container port through which a loadbalancer can communicate.
        :param container_environment: Environment that will be passed to a running container.
        :param ecs_security_groups: Security groups for ecs service in which containers are placed.
        :param ecs_subnets: Subnets to which new containers will be deployed.
        """
        self.container_name = container_name
        self.container_cpu = container_cpu
        self.container_ram = container_ram
        self.container_port = container_port
        self.container_environment = container_environment
        self.ecs_security_groups = ecs_security_groups
        self.ecs_subnets = ecs_subnets


class LoadBalancerParams():
    def __init__(
            self,
            subnets: List[aws_ec2.Subnet],
            security_groups: List[aws_ec2.SecurityGroup],
            dns: str,
            healthy_http_codes: Optional[List[int]] = None
    ):
        """
        Constructor.
        :param subnet: Subnets in which a newly created loadbalancer can operate.
        :param dns: A domain name for a loadbalancer. E.g. myweb.com. This is used to issue a new
        certificate in order a loadbalancer can use HTTPS connections.
        :param healthy_http_codes: The deployed instance is constantly pinged to determine if it is available
        (healthy) or not. Specify a list of http codes that your service can return and should be treated as healthy.
        """
        self.dns = dns
        self.security_groups = security_groups
        self.lb_subnets = subnets
        self.healthy_http_codes = healthy_http_codes


class PipelineParams:
    """
    Parameters class which specifies various parameters for ci/cd pipeline.
    """
    def __init__(self, artifact_builds_bucket: aws_s3.Bucket):
        """
        Constructor.
        :param artifact_builds_bucket: An artifacts bucket which will be used by a ci/cd pipeline to write
        and read build/source artifacts.
        """
        self.artifact_builds_bucket = artifact_builds_bucket

class MySubStack(core.Stack):

    TARGET_GROUP_PORT = 80
    LISTENER_HTTP_PORT_1 = 80
    LISTENER_HTTPS_PORT_1 = 443
    LISTENER_HTTP_PORT_2 = 8000
    LISTENER_HTTPS_PORT_2 = 44300

    def __init__(
            self, scope: core.Construct, id: str,
            prefix: str,
            region: str,
            account_id: str,
            vpc: aws_ec2.Vpc,
            lb_params: LoadBalancerParams,
            ecs_params: EcsParams,
            pipeline_params: PipelineParams,
    ) -> None:
        """
        Constructor.
        :param prefix: The prefix for all newly created resources. E.g. Wordpress.
        :param region: The region where resources and the stack are deployed.
        :param account_id: The id of the account which executes this stack.
        :param vpc: Virtual private cloud (VPC).
        :param lb_params: Loadbalancer parameters.
        :param ecs_params: Compute power parameters for newly deployed container.
        :param pipeline_params: Parameters for a ci/cd pipeline.
        """
        super().__init__(scope, id)

        self.vpc = aws_ec2.Vpc(self, 'vpc')



        self.task = aws_ecs.FargateTaskDefinition(self, "Task", cpu=256, memory_limit_mib=512, family='myfamily')
        self.container = self.task.add_container("Container", image=aws_ecs.ContainerImage.from_registry('nginx:latest'))
        self.container.add_port_mappings(aws_ecs.PortMapping(container_port=80))
        self.service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Fargate",
            cpu=256,
            memory_limit_mib=512,
            task_definition=self.task,
            load_balancer=self.load_balancer,
            assign_public_ip=True
        )
        self.scaling = self.service.service.auto_scale_task_count(max_capacity=5)
        self.scaling.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=75)

        self.myapp = aws_codedeploy.CfnApplication(
            self, 'myapp',
            application_name='fargateapp',
            compute_platform='ECS'
        )

        self.deployment_role = aws_iam.Role(
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
            assumed_by=aws_iam.ServicePrincipal('ecs-tasks.amazonaws.com')
        )

        AwsCustomResource(self, "CreateProject",
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
                              "physicalResourceId": '123'
                          },
                          )

        # myrepo = aws_codecommit.Repository(self, "Repository", repository_name="my_repository")
        # source_artifact = aws_codepipeline.Artifact()
        # build_artifact = aws_codepipeline.Artifact("BuildArtifact")
        # project = aws_codebuild.Project(
        #     self, "Project",
        #     source=aws_codebuild.Source.code_commit(repository=myrepo),
        #     build_spec=aws_codebuild.BuildSpec.from_source_filename('push-to-ecr.yml')
        # )
        #
        # pipeline = aws_codepipeline.Pipeline(self, "Pipeline")
        #
        # source = pipeline.add_stage(stage_name="Source")
        # source.add_action(
        #     aws_codepipeline_actions.CodeCommitSourceAction(
        #         branch='master',
        #         repository=myrepo,
        #         output=source_artifact,
        #         action_name="Commit"
        #     )
        # )
        #
        # build = pipeline.add_stage(stage_name="Build")
        # build.add_action(
        #     aws_codepipeline_actions.CodeBuildAction(
        #         input=source_artifact,
        #         project=project,
        #         action_name="Build",
        #         outputs=[build_artifact]
        #     )
        # )
        #
        # secondary_myrepo = aws_ecr.Repository(self, "EcrRepo")
        # secondary_source_artifact = aws_codepipeline.Artifact()
        # secondary_build_artifact = aws_codepipeline.Artifact("BuildArtifact")
        # secondary_project = aws_codebuild.Project(
        #     self, "BuildProject",
        #     build_spec=aws_codebuild.BuildSpec.from_object({'deploy': 'deploy'})
        # )
        #
        # secondary_pipeline = aws_codepipeline.Pipeline(self, "SecPipeline")
        #
        # secondary_source = secondary_pipeline.add_stage(stage_name="SecSource")
        # secondary_source.add_action(
        #     aws_codepipeline_actions.EcrSourceAction(
        #         output=secondary_source_artifact,
        #         repository=secondary_myrepo,
        #         action_name="Source"
        #     )
        # )
        #
        # secondary_build = secondary_pipeline.add_stage(stage_name="SecBuild")
        # secondary_build.add_action(
        #     aws_codepipeline_actions.CodeBuildAction(
        #         input=secondary_source_artifact,
        #         project=secondary_project,
        #         action_name="Build", outputs=[secondary_build_artifact]
        #     )
        # )
        #
        # secondary_deploy = secondary_pipeline.add_stage(stage_name="SecDeploy")
        # secondary_deploy.add_action(
        #     aws_codepipeline_actions.EcsDeployAction(
        #         service=service.service,
        #         action_name="Deploy",
        #         input=build_artifact
        #     )
        # )

    def create_task_def(self):
        """
        Creates a task definition object which will be used for deploying new containers through a pipeline.
        The task definition object specifies parameters about newly created containers.
        :return: Task definition object.
        """
        environment_list = []

        for key, value in self.environment.items():
            join = Join(delimiter='', values=['{"name": "', key, '", "value": "', value, '"}'])
            environment_list.append(join)

        environment = Join(delimiter='\n', values=[
            '"environment": [',
            Join(delimiter=',\n', values=environment_list),
            '],'
        ])

        definition = Join(delimiter='\n', values=[
            '{',
            Join(delimiter='', values=['    "executionRoleArn": ', '"', self.task.execution_role.role_arn, '"', ',']),
            '    "containerDefinitions": [',
            '        {',
            '            "name": "{}",'.format(self.container_name),
            '            "image": "<IMAGE1_NAME>",',
            '            "essential": true,',
            environment,
            # For task definitions that use the awsvpc network mode, you should only specify the containerPort.
            # The hostPort can be left blank or it must be the same value as the containerPort.
            '            "portMappings": [',
            '                {',
            '                   "containerPort": {}'.format(self.container_port),
            '                }',
            '            ],',
            '            "logConfiguration": {',
            '                "logDriver": "awslogs",',
            '                "options": {',
            '                    "awslogs-group": "{}",'.format(self.log_group.LogGroupName),
            '                    "awslogs-region": "{}",'.format(self.aws_region),
            '                    "awslogs-stream-prefix": "{}"'.format(self.prefix),
            '                }',
            '            }',
            '        }',
            '    ],',
            '    "requiresCompatibilities": [',
            '        "FARGATE"',
            '    ],',
            '    "networkMode": "awsvpc",',
            '    "cpu": "{}",'.format(self.cpu),
            '    "memory": "{}",'.format(self.ram),
            '    "family": "{}"'.format(self.prefix.lower()),
            '}'
        ])

        return definition

    def create_appspec(self):
        """
        Creates an application specification object which will be used for deploying new containers through a pipeline.
        The application specification object specifies parameters about the ECS service.
        :return: Application specification object.
        """
        app_spec = (
            f'version: 0.0',
            f'Resources:',
            f'  - TargetService:',
            f'      Type: AWS::ECS::Service',
            f'      Properties:',
            f'        TaskDefinition: <TASK_DEFINITION>',
            f'        LoadBalancerInfo:',
            f'          ContainerName: "{self.container_name}"',
            f'          ContainerPort: 80',
        )

        return '\n'.join(app_spec)