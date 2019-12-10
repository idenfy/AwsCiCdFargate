from typing import List, Optional


class VpcParameters:
    def __init__(self, subnet_ids: List[str], security_group_ids: List[str]):
        """
        Parameters for your lambda functions Virtual Private Network configuration.

        :param subnet_ids: List of subnets your function should be deployed to.
        These subnets need a NAT gateway in order for the function to to access the internet.
        :param security_group_ids: List of security group IDs for your function

        :return No return.
        """
        self.subnet_ids = VpcParameters.__list_to_comma_separated_list(subnet_ids)
        self.security_group_ids = VpcParameters.__list_to_comma_separated_list(security_group_ids)

    @staticmethod
    def __list_to_comma_separated_list(strings: List[str]) -> str:
        return ', '.join(strings)


class LambdaTypeParameters:
    def __init__(self, event_type: str, **kwargs):
        """
        Parameters, describing your function invocation event.

        :param event_type: The type of event, that invokes your function.
        Currently supported types are:
        Api - Creates an API gateway for your function with GET and POST requests.
        Schedule - Creates a schedule to invoke your lambda function at specific times.
        In this case, argument schedule_expression is also required
        None - No invocation event is created, your function can only be deployed in the AWS testing environment.
        :param kwargs: currently supported arguments:
        schedule_expression - a string, describing your lambda invocation schedule.

        Is can be either:
        rate(x units), meaning your function will be called every x units.
        e.g. rate(5 minutes), in which case the function will be invoked every 5 minutes.

        cron(Minutes Hours Day-of-month Month Day-of-week Year)
        e.g. cron(0 0 * * ? *), which would mean, that the function will be invoked every day at midnight.

        More info: https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html

        :return No return.
        """
        assert event_type in ['Api', 'Schedule', 'None']

        self.event_type = event_type
        if event_type == 'Schedule':
            self.schedule_expression = kwargs['schedule_expression']
            assert self.schedule_expression.startswith('rate(') or self.schedule_expression.startswith('cron(')


class DeploymentParameters:
    def __init__(self, project_name: str, bucket_name):
        """
        Parameters for project deployment.

        :param project_name: Name of your project, which is also used in naming most of the resources and CloudFormation stacks.
        :param bucket_name: Name of the bucket, where deployment files are located.

        :return No return.
        """
        self.project_name = project_name
        self.bucket_name = bucket_name


class CodeStarLambdaParameters:
    def __init__(self, vpc_params: VpcParameters, deployment_params: LambdaTypeParameters, lambda_type_params: DeploymentParameters):
        self.lambda_type_params = lambda_type_params
        self.deployment_params = deployment_params
        self.vpc_params = vpc_params
