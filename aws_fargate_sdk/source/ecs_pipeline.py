import re

from aws_cdk.custom_resources import AwsCustomResource
from aws_empty_bucket.empty_s3_bucket import EmptyS3Bucket
from aws_fargate_sdk.source.pipeline_commit_to_ecr import PipelineCommitToEcr
from aws_fargate_sdk.source.pipeline_ecr_to_ecs import PipelineEcrToEcs
from aws_cdk import (
    aws_ecs,
    aws_codecommit,
    aws_ecr,
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
    ) -> None:
        """
        Constructor.

        :param scope: A CloudFormation template to which add resources.
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
            self.__convert(prefix + 'FargateArtifacts'),
            access_control=aws_s3.BucketAccessControl.PRIVATE,
            bucket_name=self.__convert(prefix + 'FargateArtifacts'),
        )

        self.source_code_repository = aws_codecommit.Repository(
            scope,
            prefix + 'FargateSourceCode',
            repository_name=prefix + 'FargateSourceCode'
        )

        self.ecr_repository = aws_ecr.Repository(
            scope, prefix + 'FargateEcrRepository',
            repository_name=prefix.lower()
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
            ecs_service=ecs_service
        )

        self.commit_to_ecr = PipelineCommitToEcr(
            scope=scope,
            prefix=prefix,
            artifacts_bucket=self.artifacts_bucket,
            ecr_repository=self.ecr_repository,
            source_repository=self.source_code_repository,
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
