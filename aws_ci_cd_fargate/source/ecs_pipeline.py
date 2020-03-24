import re

from typing import Any, Dict
from aws_cdk.core import RemovalPolicy
from aws_cdk.custom_resources import AwsCustomResource
from aws_empty_bucket.empty_s3_bucket import EmptyS3Bucket
from aws_empty_ecr_repository.empty_ecr_repository import EmptyEcrRepository
from aws_ci_cd_fargate.source.pipeline_commit_to_ecr import PipelineCommitToEcr
from aws_ci_cd_fargate.source.pipeline_ecr_to_ecs import PipelineEcrToEcs
from aws_cdk import (
    aws_ecs,
    aws_codecommit,
    aws_elasticloadbalancingv2,
    aws_s3,
    core
)


class EcsPipeline:
    """
    Class which creates infrastructure for CI/CD Blue/Green Ecs Fargate deployments.
    """
    def __init__(
            self,
            scope: core.Stack,
            prefix: str,
            main_listener: aws_elasticloadbalancingv2.CfnListener,
            deployments_listener: aws_elasticloadbalancingv2.CfnListener,
            ecs_service: AwsCustomResource,
            ecs_cluster: aws_ecs.Cluster,
            task_def: str,
            app_spec: str,
            build_environment: Dict[str, Any],
            docker_build_args: Dict[str, str],
            production_target_group,
            deployment_target_group
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation template to which add resources.
        :param prefix: A prefix for newly created resources.
        :param main_listener: A listener which receives incoming traffic and forwards it to a target group.
        :param deployments_listener: A listener which receives incoming traffic and forwards it to a target group.
        This listener is used for blue/green deployment.
        :param ecs_service: Ecs service to which create this pipeline.
        :param ecs_cluster: ECS cluster in which the ECS service is.
        :param task_def: Task definition object defining the parameters for a newly deployed container.
        :param app_spec: App specification object defining the ecs service modifications.
        :param build_environment: Environment variables for a build step. You can put here various config
        parameters, urls, secrets, etc.
        :param docker_build_args: Build arguments for docker build command.
        :param production_target_group: A target group where your blue instances are serving production traffic.
        :param deployment_target_group: A target group where your green instances are ready to serve production traffic.
        """
        self.artifacts_bucket = EmptyS3Bucket(
            scope,
            self.__convert(prefix + 'FargateArtifacts'),
            access_control=aws_s3.BucketAccessControl.PRIVATE,
            bucket_name=self.__convert(prefix + 'FargateArtifacts'),
        )

        self.source_code_repository = aws_codecommit.Repository(
            scope,
            prefix + 'FargateSourceCode',
            repository_name=prefix + 'FargateSourceCode'
        )

        self.ecr_repository = EmptyEcrRepository(
            scope, prefix + 'FargateEcrRepository',
            repository_name=prefix.lower(),
            removal_policy=RemovalPolicy.DESTROY
        )

        self.ecr_to_ecs = PipelineEcrToEcs(
            scope=scope,
            prefix=prefix,
            artifacts_bucket=self.artifacts_bucket,
            source_repository=self.source_code_repository,
            ecr_repository=self.ecr_repository,
            task_def=task_def,
            app_spec=app_spec,
            main_listener=main_listener,
            deployments_listener=deployments_listener,
            ecs_cluster=ecs_cluster,
            ecs_service=ecs_service,
            production_target_group=production_target_group,
            deployment_target_group=deployment_target_group
        )

        self.commit_to_ecr = PipelineCommitToEcr(
            scope=scope,
            prefix=prefix,
            artifacts_bucket=self.artifacts_bucket,
            ecr_repository=self.ecr_repository,
            source_repository=self.source_code_repository,
            build_environment=build_environment,
            docker_build_args=docker_build_args,
            next_pipeline=self.ecr_to_ecs.ecr_to_ecs_pipeline
        )

    @staticmethod
    def __convert(name: str) -> str:
        """
        Converts CamelCase string to pascal-case where underscores are dashes.
        This is required due to S3 not supporting capital letters or underscores.
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()
