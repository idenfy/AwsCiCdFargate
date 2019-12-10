from aws_cdk import core, aws_ecs, aws_codedeploy, aws_codecommit, aws_codebuild, aws_codepipeline, \
    aws_codepipeline_actions, aws_ecr, aws_ecs_patterns, aws_elasticloadbalancingv2, aws_ec2, aws_certificatemanager, aws_iam


class MySubStack(core.Stack):

    TARGET_GROUP_PORT = 80
    LISTENER_HTTP_PORT_1 = 80
    LISTENER_HTTPS_PORT_1 = 443
    LISTENER_HTTP_PORT_2 = 8000
    LISTENER_HTTPS_PORT_2 = 44300

    def __init__(self, scope: core.Construct, id: str, desired_domain_name: str) -> None:
        super().__init__(scope, id)

        vpc = aws_ec2.Vpc(self, 'vpc')

        certificate = aws_certificatemanager.Certificate(self, 'cert', domain_name=desired_domain_name, validation_method=aws_certificatemanager.ValidationMethod.DNS)

        load_balancer = aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, 'load_balancer', vpc=vpc
        )
        http_listener_1 = load_balancer.add_listener(
            'listener1',
            port=self.LISTENER_HTTP_PORT_1,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP
        )
        http_listener_1.add_redirect_response(
            'https-redirect',
            host='#{host}',
            path='/#{path}',
            port=str(self.LISTENER_HTTPS_PORT_1),
            query='#{query}',
            status_code='HTTP_301',
            protocol='HTTPS'
        )

        http_target_group_1 = aws_elasticloadbalancingv2.ApplicationTargetGroup(
            self, 'target_group1',
            port=self.TARGET_GROUP_PORT,
            vpc=vpc,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            target_type=aws_elasticloadbalancingv2.TargetType.IP,
            health_check=aws_elasticloadbalancingv2.HealthCheck()
        )

        https_listener_1 = load_balancer.add_listener(
            'listener2',
            port=self.LISTENER_HTTPS_PORT_1,
            certificate_arns=[certificate.certificate_arn],
            default_target_groups=[http_target_group_1],
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS
        )

        http_listener_2 = load_balancer.add_listener(
            'listener3',
            port=self.LISTENER_HTTP_PORT_2,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP
        )

        http_listener_2.add_redirect_response(
            'https-redirect',
            host='#{host}',
            path='/#{path}',
            port=str(self.LISTENER_HTTPS_PORT_2),
            query='#{query}',
            status_code='HTTP_301',
            protocol='HTTPS'
        )

        http_target_group_2 = aws_elasticloadbalancingv2.ApplicationTargetGroup(
            self, 'target_group2',
            port=self.TARGET_GROUP_PORT,
            vpc=vpc,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            target_type=aws_elasticloadbalancingv2.TargetType.IP,
            health_check=aws_elasticloadbalancingv2.HealthCheck()
        )
        https_listener_2 = load_balancer.add_listener(
            'listener4',
            port=self.LISTENER_HTTPS_PORT_2,
            certificate_arns=[certificate.certificate_arn],
            default_target_groups=[http_target_group_2],
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS
        )

        task = aws_ecs.FargateTaskDefinition(self, "Task", cpu=256, memory_limit_mib=512, family='myfamily')
        container = task.add_container("Container", image=aws_ecs.ContainerImage.from_registry('nginx:latest'))
        container.add_port_mappings(aws_ecs.PortMapping(container_port=80))
        service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "Fargate",
            cpu=256,
            memory_limit_mib=512,
            task_definition=task,
            load_balancer=load_balancer,
            assign_public_ip=True
        )
        scaling = service.service.auto_scale_task_count(max_capacity=5)
        scaling.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=75)

        myapp = aws_codedeploy.CfnApplication(
            self, 'myapp',
            application_name='fargateapp',
            compute_platform='ECS'
        )

        deployment_role = aws_iam.Role(
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

        aws_codedeploy.CfnDeploymentGroup(
            self, 'DeploymentGroup',
            service_role_arn=deployment_role.role_arn,
            application_name=myapp.application_name,
            deployment_group_name='mydeploymentgroup',
            deployment_config_name='CodeDeployDefault.ECSAllAtOnce'
        )

        myrepo = aws_codecommit.Repository(self, "Repository", repository_name="my_repository")
        source_artifact = aws_codepipeline.Artifact()
        build_artifact = aws_codepipeline.Artifact("BuildArtifact")
        project = aws_codebuild.Project(
            self, "Project",
            source=aws_codebuild.Source.code_commit(repository=myrepo),
            build_spec=aws_codebuild.BuildSpec.from_source_filename('push-to-ecr.yml')
        )

        pipeline = aws_codepipeline.Pipeline(self, "Pipeline")

        source = pipeline.add_stage(stage_name="Source")
        source.add_action(
            aws_codepipeline_actions.CodeCommitSourceAction(
                branch='master',
                repository=myrepo,
                output=source_artifact,
                action_name="Commit"
            )
        )

        build = pipeline.add_stage(stage_name="Build")
        build.add_action(
            aws_codepipeline_actions.CodeBuildAction(
                input=source_artifact,
                project=project,
                action_name="Build",
                outputs=[build_artifact]
            )
        )

        secondary_myrepo = aws_ecr.Repository(self, "EcrRepo")
        secondary_source_artifact = aws_codepipeline.Artifact()
        secondary_build_artifact = aws_codepipeline.Artifact("BuildArtifact")
        secondary_project = aws_codebuild.Project(
            self, "BuildProject",
            build_spec=aws_codebuild.BuildSpec.from_object({'deploy': 'deploy'})
        )

        secondary_pipeline = aws_codepipeline.Pipeline(self, "SecPipeline")

        secondary_source = secondary_pipeline.add_stage(stage_name="SecSource")
        secondary_source.add_action(
            aws_codepipeline_actions.EcrSourceAction(
                output=secondary_source_artifact,
                repository=secondary_myrepo,
                action_name="Source"
            )
        )

        secondary_build = secondary_pipeline.add_stage(stage_name="SecBuild")
        secondary_build.add_action(
            aws_codepipeline_actions.CodeBuildAction(
                input=secondary_source_artifact,
                project=secondary_project,
                action_name="Build", outputs=[secondary_build_artifact]
            )
        )

        secondary_deploy = secondary_pipeline.add_stage(stage_name="SecDeploy")
        secondary_deploy.add_action(
            aws_codepipeline_actions.EcsDeployAction(
                service=service.service,
                action_name="Deploy",
                input=build_artifact
            )
        )
