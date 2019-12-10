import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/custom-resources", "1.15.0", __name__, "custom-resources@1.15.0.jsii.tgz")
class AwsCustomResource(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/custom-resources.AwsCustomResource"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, on_create: typing.Optional["AwsSdkCall"]=None, on_delete: typing.Optional["AwsSdkCall"]=None, on_update: typing.Optional["AwsSdkCall"]=None, policy_statements: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param on_create: The AWS SDK call to make when the resource is created. At least onCreate, onUpdate or onDelete must be specified. Default: the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: no call
        :param policy_statements: The IAM policy statements to allow the different calls. Use only if resource restriction is needed. Default: extract the permissions from the calls
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        props = AwsCustomResourceProps(on_create=on_create, on_delete=on_delete, on_update=on_update, policy_statements=policy_statements, timeout=timeout)

        jsii.create(AwsCustomResource, self, [scope, id, props])

    @jsii.member(jsii_name="getData")
    def get_data(self, data_path: str) -> aws_cdk.core.Reference:
        """Returns response data for the AWS SDK call.

        Example for S3 / listBucket : 'Buckets.0.Name'

        :param data_path: the path to the data.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getData", [data_path])


@jsii.data_type(jsii_type="@aws-cdk/custom-resources.AwsCustomResourceProps", jsii_struct_bases=[], name_mapping={'on_create': 'onCreate', 'on_delete': 'onDelete', 'on_update': 'onUpdate', 'policy_statements': 'policyStatements', 'timeout': 'timeout'})
class AwsCustomResourceProps():
    def __init__(self, *, on_create: typing.Optional["AwsSdkCall"]=None, on_delete: typing.Optional["AwsSdkCall"]=None, on_update: typing.Optional["AwsSdkCall"]=None, policy_statements: typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]=None, timeout: typing.Optional[aws_cdk.core.Duration]=None):
        """
        :param on_create: The AWS SDK call to make when the resource is created. At least onCreate, onUpdate or onDelete must be specified. Default: the call when the resource is updated
        :param on_delete: The AWS SDK call to make when the resource is deleted. Default: no call
        :param on_update: The AWS SDK call to make when the resource is updated. Default: no call
        :param policy_statements: The IAM policy statements to allow the different calls. Use only if resource restriction is needed. Default: extract the permissions from the calls
        :param timeout: The timeout for the Lambda function implementing this custom resource. Default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        self._values = {
        }
        if on_create is not None: self._values["on_create"] = on_create
        if on_delete is not None: self._values["on_delete"] = on_delete
        if on_update is not None: self._values["on_update"] = on_update
        if policy_statements is not None: self._values["policy_statements"] = policy_statements
        if timeout is not None: self._values["timeout"] = timeout

    @property
    def on_create(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is created. At least onCreate, onUpdate or onDelete must be specified.

        default
        :default: the call when the resource is updated

        stability
        :stability: experimental
        """
        return self._values.get('on_create')

    @property
    def on_delete(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is deleted.

        default
        :default: no call

        stability
        :stability: experimental
        """
        return self._values.get('on_delete')

    @property
    def on_update(self) -> typing.Optional["AwsSdkCall"]:
        """The AWS SDK call to make when the resource is updated.

        default
        :default: no call

        stability
        :stability: experimental
        """
        return self._values.get('on_update')

    @property
    def policy_statements(self) -> typing.Optional[typing.List[aws_cdk.aws_iam.PolicyStatement]]:
        """The IAM policy statements to allow the different calls.

        Use only if
        resource restriction is needed.

        default
        :default: extract the permissions from the calls

        stability
        :stability: experimental
        """
        return self._values.get('policy_statements')

    @property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The timeout for the Lambda function implementing this custom resource.

        default
        :default: Duration.seconds(30)

        stability
        :stability: experimental
        """
        return self._values.get('timeout')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsCustomResourceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/custom-resources.AwsSdkCall", jsii_struct_bases=[], name_mapping={'action': 'action', 'service': 'service', 'api_version': 'apiVersion', 'catch_error_pattern': 'catchErrorPattern', 'output_path': 'outputPath', 'parameters': 'parameters', 'physical_resource_id': 'physicalResourceId', 'physical_resource_id_path': 'physicalResourceIdPath', 'region': 'region'})
class AwsSdkCall():
    def __init__(self, *, action: str, service: str, api_version: typing.Optional[str]=None, catch_error_pattern: typing.Optional[str]=None, output_path: typing.Optional[str]=None, parameters: typing.Any=None, physical_resource_id: typing.Optional[str]=None, physical_resource_id_path: typing.Optional[str]=None, region: typing.Optional[str]=None):
        """An AWS SDK call.

        :param action: The service action to call.
        :param service: The service to call.
        :param api_version: API version to use for the service. Default: - use latest available API version
        :param catch_error_pattern: The regex pattern to use to catch API errors. The ``code`` property of the ``Error`` object will be tested against this pattern. If there is a match an error will not be thrown. Default: - do not catch errors
        :param output_path: Restrict the data returned by the custom resource to a specific path in the API response. Use this to limit the data returned by the custom resource if working with API calls that could potentially result in custom response objects exceeding the hard limit of 4096 bytes. Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent' Default: return all data
        :param parameters: The parameters for the service action.
        :param physical_resource_id: The physical resource id of the custom resource for this call. Either ``physicalResourceId`` or ``physicalResourceIdPath`` must be specified for onCreate or onUpdate calls. Default: - no physical resource id
        :param physical_resource_id_path: The path to the data in the API call response to use as the physical resource id. Either ``physicalResourceId`` or ``physicalResourceIdPath`` must be specified for onCreate or onUpdate calls. Default: - no path
        :param region: The region to send service requests to. **Note: Cross-region operations are generally considered an anti-pattern.** **Consider first deploying a stack in that region.**. Default: - the region where this custom resource is deployed

        stability
        :stability: experimental
        """
        self._values = {
            'action': action,
            'service': service,
        }
        if api_version is not None: self._values["api_version"] = api_version
        if catch_error_pattern is not None: self._values["catch_error_pattern"] = catch_error_pattern
        if output_path is not None: self._values["output_path"] = output_path
        if parameters is not None: self._values["parameters"] = parameters
        if physical_resource_id is not None: self._values["physical_resource_id"] = physical_resource_id
        if physical_resource_id_path is not None: self._values["physical_resource_id_path"] = physical_resource_id_path
        if region is not None: self._values["region"] = region

    @property
    def action(self) -> str:
        """The service action to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('action')

    @property
    def service(self) -> str:
        """The service to call.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('service')

    @property
    def api_version(self) -> typing.Optional[str]:
        """API version to use for the service.

        default
        :default: - use latest available API version

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/locking-api-versions.html
        stability
        :stability: experimental
        """
        return self._values.get('api_version')

    @property
    def catch_error_pattern(self) -> typing.Optional[str]:
        """The regex pattern to use to catch API errors.

        The ``code`` property of the
        ``Error`` object will be tested against this pattern. If there is a match an
        error will not be thrown.

        default
        :default: - do not catch errors

        stability
        :stability: experimental
        """
        return self._values.get('catch_error_pattern')

    @property
    def output_path(self) -> typing.Optional[str]:
        """Restrict the data returned by the custom resource to a specific path in the API response.

        Use this to limit the data returned by the custom
        resource if working with API calls that could potentially result in custom
        response objects exceeding the hard limit of 4096 bytes.

        Example for ECS / updateService: 'service.deploymentConfiguration.maximumPercent'

        default
        :default: return all data

        stability
        :stability: experimental
        """
        return self._values.get('output_path')

    @property
    def parameters(self) -> typing.Any:
        """The parameters for the service action.

        see
        :see: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/index.html
        stability
        :stability: experimental
        """
        return self._values.get('parameters')

    @property
    def physical_resource_id(self) -> typing.Optional[str]:
        """The physical resource id of the custom resource for this call.

        Either
        ``physicalResourceId`` or ``physicalResourceIdPath`` must be specified for
        onCreate or onUpdate calls.

        default
        :default: - no physical resource id

        stability
        :stability: experimental
        """
        return self._values.get('physical_resource_id')

    @property
    def physical_resource_id_path(self) -> typing.Optional[str]:
        """The path to the data in the API call response to use as the physical resource id.

        Either ``physicalResourceId`` or ``physicalResourceIdPath``
        must be specified for onCreate or onUpdate calls.

        default
        :default: - no path

        stability
        :stability: experimental
        """
        return self._values.get('physical_resource_id_path')

    @property
    def region(self) -> typing.Optional[str]:
        """The region to send service requests to. **Note: Cross-region operations are generally considered an anti-pattern.** **Consider first deploying a stack in that region.**.

        default
        :default: - the region where this custom resource is deployed

        stability
        :stability: experimental
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AwsSdkCall(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AwsCustomResource", "AwsCustomResourceProps", "AwsSdkCall", "__jsii_assembly__"]

publication.publish()
