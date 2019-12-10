from aws_cdk import core, aws_iam
from aws_cdk.custom_resources import AwsCustomResource
from aws_codestar_cdk.cdk_stack.parameters import CodeStarLambdaParameters


class CodeStarStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, params: CodeStarLambdaParameters) -> None:
        super().__init__(scope, id)

        policy = aws_iam.PolicyStatement(
            actions=[
                "iam:PassRole",
                "codestar:CreateProject",
                "codestar:UpdateProject",
                "codestar:DeleteProject",
                "s3:GetObject"
            ]
        )
        policy.add_all_resources()

        # Deployment parameters.
        project_name = params.deployment_params.project_name
        bucket_name = params.deployment_params.bucket_name

        # S3 file keys, which coincide with file names in files/ folder.
        code_bucket_key = 'source.zip'
        toolchain_bucket_key = 'toolchain.yml'

        # VPC parameters for lambda function.
        subnet_ids = params.vpc_params.subnet_ids
        security_group_ids = params.vpc_params.security_group_ids

        # Parameters for function invocation
        event_type = params.lambda_type_params.event_type

        stack_parameters = {
            "ProjectId": project_name,
            "MySubnetIds": subnet_ids,
            "MySecurityGroupIds": security_group_ids,
            "EventType": event_type
        }

        if event_type == 'Schedule':
            schedule_expression = params.lambda_type_params.schedule_expression
            stack_parameters["ScheduleExpression"] = schedule_expression

        AwsCustomResource(self, "CreateProject",
                          on_create={
                              "service": "CodeStar",
                              "action": "createProject",
                              "parameters": {
                                  'id': project_name,
                                  'name': project_name,
                                  'sourceCode': [
                                      {
                                          'destination': {
                                              'codeCommit': {
                                                  'name': project_name
                                              },
                                          },
                                          'source': {
                                              's3': {
                                                  'bucketKey': code_bucket_key,
                                                  'bucketName': bucket_name
                                              }
                                          }
                                      },
                                  ],
                                  'toolchain': {
                                      'source': {
                                          's3': {
                                              'bucketKey': toolchain_bucket_key,
                                              'bucketName': bucket_name
                                          }
                                      },
                                      'roleArn': 'arn:aws:iam::770536902058:role/service-role/aws-codestar-service-role',
                                      'stackParameters': stack_parameters
                                  }
                              },
                              "physicalResourceId": '123'
                          },
                          on_update={
                              "service": "CodeStar",
                              "action": "updateProject",
                              "parameters": {
                                  'id': project_name,
                                  "description": "dummy description",
                              },
                              "physicalResourceId": '123'
                          },
                          on_delete={
                              "service": "CodeStar",
                              "action": "deleteProject",
                              "parameters": {
                                  'id': project_name,
                                  "deleteStack": True,
                              },
                              "physicalResourceId": '123'
                          },
                          policy_statements=[policy]
                          )
