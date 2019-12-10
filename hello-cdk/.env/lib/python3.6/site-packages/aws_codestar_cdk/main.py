from aws_codestar_cdk.cdk_stack.stack import CodeStarStack
from aws_codestar_cdk.cdk_stack.parameters import CodeStarLambdaParameters, VpcParameters, LambdaTypeParameters, DeploymentParameters
from aws_codestar_cdk.cdk_stack.bucket_stack import DeploymentBucketStack
from typing import List, Optional
from aws_cdk import core


class LambdaCodeStar:

    def __init__(self, scope: core.Construct, vpc_params: VpcParameters, deployment_params: LambdaTypeParameters, lambda_type_params: DeploymentParameters):
        bucket_stack = DeploymentBucketStack(scope, '{}-bucket-stack'.format(deployment_params.project_name), deployment_params.bucket_name)
        parameters = CodeStarLambdaParameters(vpc_params, deployment_params, lambda_type_params)
        self.__stack = CodeStarStack(scope, '{}-stack'.format(deployment_params.project_name), parameters)
        self.__stack.add_dependency(bucket_stack)

    def get_stack(self):
        return self.__stack
