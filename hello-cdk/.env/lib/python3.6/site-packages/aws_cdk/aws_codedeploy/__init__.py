"""
## AWS CodeDeploy Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

AWS CodeDeploy is a deployment service that automates application deployments to
Amazon EC2 instances, on-premises instances, serverless Lambda functions, or
Amazon ECS services.

The CDK currently supports Amazon EC2, on-premise and AWS Lambda applications.

### EC2/on-premise Applications

To create a new CodeDeploy Application that deploys to EC2/on-premise instances:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codedeploy as codedeploy

application = codedeploy.ServerApplication(self, "CodeDeployApplication",
    application_name="MyApplication"
)
```

To import an already existing Application:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
application = codedeploy.ServerApplication.from_server_application_name(self, "ExistingCodeDeployApplication", "MyExistingApplication")
```

### EC2/on-premise Deployment Groups

To create a new CodeDeploy Deployment Group that deploys to EC2/on-premise instances:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyDeploymentGroup",
    auto_scaling_groups=[asg1, asg2],
    # adds User Data that installs the CodeDeploy agent on your auto-scaling groups hosts
    # default: true
    install_agent=True,
    # adds EC2 instances matching tags
    ec2_instance_tags=codedeploy.InstanceTagSet(
        # any instance with tags satisfying
        # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
        # will match this group
        key1=["v1", "v2"],
        key2=[],
        =["v3"]
    ),
    # adds on-premise instances matching tags
    on_premise_instance_tags=codedeploy.InstanceTagSet({
        "key1": ["v1", "v2"]
    },
        key2=["v3"]
    ),
    # CloudWatch alarms
    alarms=[
        cloudwatch.Alarm()
    ],
    # whether to ignore failure to fetch the status of alarms from CloudWatch
    # default: false
    ignore_poll_alarms_failure=False,
    # auto-rollback configuration
    auto_rollback={
        "failed_deployment": True, # default: true
        "stopped_deployment": True, # default: false
        "deployment_in_alarm": True
    }
)
```

All properties are optional - if you don't provide an Application,
one will be automatically created.

To import an already existing Deployment Group:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.ServerDeploymentGroup.from_lambda_deployment_group_attributes(self, "ExistingCodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyExistingDeploymentGroup"
)
```

#### Load balancers

You can [specify a load balancer](https://docs.aws.amazon.com/codedeploy/latest/userguide/integrations-aws-elastic-load-balancing.html)
with the `loadBalancer` property when creating a Deployment Group.

`LoadBalancer` is an abstract class with static factory methods that allow you to create instances of it from various sources.

With Classic Elastic Load Balancer, you provide it directly:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancing as lb

elb = lb.LoadBalancer(self, "ELB")
elb.add_target()
elb.add_listener()

deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
    load_balancer=codedeploy.LoadBalancer.classic(elb)
)
```

With Application Load Balancer or Network Load Balancer,
you provide a Target Group as the load balancer:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticloadbalancingv2 as lbv2

alb = lbv2.ApplicationLoadBalancer(self, "ALB")
listener = alb.add_listener("Listener")
target_group = listener.add_targets("Fleet")

deployment_group = codedeploy.ServerDeploymentGroup(self, "DeploymentGroup",
    load_balancer=codedeploy.LoadBalancer.application(target_group)
)
```

### Deployment Configurations

You can also pass a Deployment Configuration when creating the Deployment Group:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
    deployment_config=codedeploy.ServerDeploymentConfig.ALL_AT_ONCE
)
```

The default Deployment Configuration is `ServerDeploymentConfig.ONE_AT_A_TIME`.

You can also create a custom Deployment Configuration:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_config = codedeploy.ServerDeploymentConfig(self, "DeploymentConfiguration",
    deployment_config_name="MyDeploymentConfiguration", # optional property
    # one of these is required, but both cannot be specified at the same time
    min_healthy_host_count=2,
    min_healthy_host_percentage=75
)
```

Or import an existing one:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_config = codedeploy.ServerDeploymentConfig.from_server_deployment_config_name(self, "ExistingDeploymentConfiguration", "MyExistingDeploymentConfiguration")
```

### Lambda Applications

To create a new CodeDeploy Application that deploys to a Lambda function:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codedeploy as codedeploy

application = codedeploy.LambdaApplication(self, "CodeDeployApplication",
    application_name="MyApplication"
)
```

To import an already existing Application:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
application = codedeploy.LambdaApplication.from_lambda_application_name(self, "ExistingCodeDeployApplication", "MyExistingApplication")
```

### Lambda Deployment Groups

To enable traffic shifting deployments for Lambda functions, CodeDeploy uses Lambda Aliases, which can balance incoming traffic between two different versions of your function.
Before deployment, the alias sends 100% of invokes to the version used in production.
When you publish a new version of the function to your stack, CodeDeploy will send a small percentage of traffic to the new version, monitor, and validate before shifting 100% of traffic to the new version.

To create a new CodeDeploy Deployment Group that deploys to a Lambda function:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_lambda as lambda

my_application = codedeploy.LambdaApplication()
func = lambda.Function()
version = func.add_version("1")
version1_alias = lambda.Alias(self, "alias",
    alias_name="prod",
    version=version
)

deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    application=my_application, # optional property: one will be created for you if not provided
    alias=version1_alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE
)
```

In order to deploy a new version of this function:

1. Increment the version, e.g. `const version = func.addVersion('2')`.
2. Re-deploy the stack (this will trigger a deployment).
3. Monitor the CodeDeploy deployment as traffic shifts between the versions.

#### Rollbacks and Alarms

CodeDeploy will roll back if the deployment fails. You can optionally trigger a rollback when one or more alarms are in a failed state:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    alarms=[
        # pass some alarms when constructing the deployment group
        cloudwatch.Alarm(stack, "Errors",
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=1,
            evaluation_periods=1,
            metric=alias.metric_errors()
        )
    ]
)

# or add alarms to an existing group
deployment_group.add_alarm(cloudwatch.Alarm(stack, "BlueGreenErrors",
    comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
    threshold=1,
    evaluation_periods=1,
    metric=blue_green_alias.metric_errors()
))
```

#### Pre and Post Hooks

CodeDeploy allows you to run an arbitrary Lambda function before traffic shifting actually starts (PreTraffic Hook) and after it completes (PostTraffic Hook).
With either hook, you have the opportunity to run logic that determines whether the deployment must succeed or fail.
For example, with PreTraffic hook you could run integration tests against the newly created Lambda version (but not serving traffic). With PostTraffic hook, you could run end-to-end validation checks.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
warm_up_user_cache = lambda.Function()
end_to_end_validation = lambda.Function()

# pass a hook whe creating the deployment group
deployment_group = codedeploy.LambdaDeploymentGroup(stack, "BlueGreenDeployment",
    alias=alias,
    deployment_config=codedeploy.LambdaDeploymentConfig.LINEAR_10PERCENT_EVERY_1MINUTE,
    pre_hook=warm_up_user_cache
)

# or configure one on an existing deployment group
deployment_group.on_post_hook(end_to_end_validation)
```

#### Import an existing Deployment Group

To import an already existing Deployment Group:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
deployment_group = codedeploy.LambdaDeploymentGroup.import(self, "ExistingCodeDeployDeploymentGroup",
    application=application,
    deployment_group_name="MyExistingDeploymentGroup"
)
```
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codedeploy", "1.18.0", __name__, "aws-codedeploy@1.18.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.AutoRollbackConfig", jsii_struct_bases=[], name_mapping={'deployment_in_alarm': 'deploymentInAlarm', 'failed_deployment': 'failedDeployment', 'stopped_deployment': 'stoppedDeployment'})
class AutoRollbackConfig():
    def __init__(self, *, deployment_in_alarm: typing.Optional[bool]=None, failed_deployment: typing.Optional[bool]=None, stopped_deployment: typing.Optional[bool]=None):
        """The configuration for automatically rolling back deployments in a given Deployment Group.

        :param deployment_in_alarm: Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off. Default: true if you've provided any Alarms with the ``alarms`` property, false otherwise
        :param failed_deployment: Whether to automatically roll back a deployment that fails. Default: true
        :param stopped_deployment: Whether to automatically roll back a deployment that was manually stopped. Default: false
        """
        self._values = {
        }
        if deployment_in_alarm is not None: self._values["deployment_in_alarm"] = deployment_in_alarm
        if failed_deployment is not None: self._values["failed_deployment"] = failed_deployment
        if stopped_deployment is not None: self._values["stopped_deployment"] = stopped_deployment

    @property
    def deployment_in_alarm(self) -> typing.Optional[bool]:
        """Whether to automatically roll back a deployment during which one of the configured CloudWatch alarms for this Deployment Group went off.

        default
        :default: true if you've provided any Alarms with the ``alarms`` property, false otherwise
        """
        return self._values.get('deployment_in_alarm')

    @property
    def failed_deployment(self) -> typing.Optional[bool]:
        """Whether to automatically roll back a deployment that fails.

        default
        :default: true
        """
        return self._values.get('failed_deployment')

    @property
    def stopped_deployment(self) -> typing.Optional[bool]:
        """Whether to automatically roll back a deployment that was manually stopped.

        default
        :default: false
        """
        return self._values.get('stopped_deployment')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AutoRollbackConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnApplication(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.CfnApplication"):
    """A CloudFormation ``AWS::CodeDeploy::Application``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, application_name: typing.Optional[str]=None, compute_platform: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CodeDeploy::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param application_name: ``AWS::CodeDeploy::Application.ApplicationName``.
        :param compute_platform: ``AWS::CodeDeploy::Application.ComputePlatform``.
        """
        props = CfnApplicationProps(application_name=application_name, compute_platform=compute_platform)

        jsii.create(CfnApplication, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: typing.Optional[str]):
        return jsii.set(self, "applicationName", value)

    @property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        """
        return jsii.get(self, "computePlatform")

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[str]):
        return jsii.set(self, "computePlatform", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName', 'compute_platform': 'computePlatform'})
class CfnApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None, compute_platform: typing.Optional[str]=None):
        """Properties for defining a ``AWS::CodeDeploy::Application``.

        :param application_name: ``AWS::CodeDeploy::Application.ApplicationName``.
        :param compute_platform: ``AWS::CodeDeploy::Application.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name
        if compute_platform is not None: self._values["compute_platform"] = compute_platform

    @property
    def application_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-applicationname
        """
        return self._values.get('application_name')

    @property
    def compute_platform(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::Application.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-application.html#cfn-codedeploy-application-computeplatform
        """
        return self._values.get('compute_platform')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeploymentConfig(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig"):
    """A CloudFormation ``AWS::CodeDeploy::DeploymentConfig``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeDeploy::DeploymentConfig
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, deployment_config_name: typing.Optional[str]=None, minimum_healthy_hosts: typing.Optional[typing.Union[typing.Optional["MinimumHealthyHostsProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None) -> None:
        """Create a new ``AWS::CodeDeploy::DeploymentConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.
        :param minimum_healthy_hosts: ``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.
        """
        props = CfnDeploymentConfigProps(deployment_config_name=deployment_config_name, minimum_healthy_hosts=minimum_healthy_hosts)

        jsii.create(CfnDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        """
        return jsii.get(self, "deploymentConfigName")

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[str]):
        return jsii.set(self, "deploymentConfigName", value)

    @property
    @jsii.member(jsii_name="minimumHealthyHosts")
    def minimum_healthy_hosts(self) -> typing.Optional[typing.Union[typing.Optional["MinimumHealthyHostsProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        """
        return jsii.get(self, "minimumHealthyHosts")

    @minimum_healthy_hosts.setter
    def minimum_healthy_hosts(self, value: typing.Optional[typing.Union[typing.Optional["MinimumHealthyHostsProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "minimumHealthyHosts", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfig.MinimumHealthyHostsProperty", jsii_struct_bases=[], name_mapping={'type': 'type', 'value': 'value'})
    class MinimumHealthyHostsProperty():
        def __init__(self, *, type: str, value: jsii.Number):
            """
            :param type: ``CfnDeploymentConfig.MinimumHealthyHostsProperty.Type``.
            :param value: ``CfnDeploymentConfig.MinimumHealthyHostsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html
            """
            self._values = {
                'type': type,
                'value': value,
            }

        @property
        def type(self) -> str:
            """``CfnDeploymentConfig.MinimumHealthyHostsProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-type
            """
            return self._values.get('type')

        @property
        def value(self) -> jsii.Number:
            """``CfnDeploymentConfig.MinimumHealthyHostsProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentconfig-minimumhealthyhosts.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MinimumHealthyHostsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentConfigProps", jsii_struct_bases=[], name_mapping={'deployment_config_name': 'deploymentConfigName', 'minimum_healthy_hosts': 'minimumHealthyHosts'})
class CfnDeploymentConfigProps():
    def __init__(self, *, deployment_config_name: typing.Optional[str]=None, minimum_healthy_hosts: typing.Optional[typing.Union[typing.Optional["CfnDeploymentConfig.MinimumHealthyHostsProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None):
        """Properties for defining a ``AWS::CodeDeploy::DeploymentConfig``.

        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.
        :param minimum_healthy_hosts: ``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html
        """
        self._values = {
        }
        if deployment_config_name is not None: self._values["deployment_config_name"] = deployment_config_name
        if minimum_healthy_hosts is not None: self._values["minimum_healthy_hosts"] = minimum_healthy_hosts

    @property
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentConfig.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-deploymentconfigname
        """
        return self._values.get('deployment_config_name')

    @property
    def minimum_healthy_hosts(self) -> typing.Optional[typing.Union[typing.Optional["CfnDeploymentConfig.MinimumHealthyHostsProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeDeploy::DeploymentConfig.MinimumHealthyHosts``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentconfig.html#cfn-codedeploy-deploymentconfig-minimumhealthyhosts
        """
        return self._values.get('minimum_healthy_hosts')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDeploymentGroup(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup"):
    """A CloudFormation ``AWS::CodeDeploy::DeploymentGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeDeploy::DeploymentGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, application_name: str, service_role_arn: str, alarm_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AlarmConfigurationProperty"]]]=None, auto_rollback_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AutoRollbackConfigurationProperty"]]]=None, auto_scaling_groups: typing.Optional[typing.List[str]]=None, deployment: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentProperty"]]]=None, deployment_config_name: typing.Optional[str]=None, deployment_group_name: typing.Optional[str]=None, deployment_style: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentStyleProperty"]]]=None, ec2_tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EC2TagFilterProperty"]]]]]=None, ec2_tag_set: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EC2TagSetProperty"]]]=None, load_balancer_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoadBalancerInfoProperty"]]]=None, on_premises_instance_tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TagFilterProperty"]]]]]=None, on_premises_tag_set: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["OnPremisesTagSetProperty"]]]=None, trigger_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TriggerConfigProperty"]]]]]=None) -> None:
        """Create a new ``AWS::CodeDeploy::DeploymentGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param application_name: ``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.
        :param service_role_arn: ``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.
        :param alarm_configuration: ``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.
        :param auto_rollback_configuration: ``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.
        :param auto_scaling_groups: ``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.
        :param deployment: ``AWS::CodeDeploy::DeploymentGroup.Deployment``.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.
        :param deployment_group_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.
        :param deployment_style: ``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.
        :param ec2_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.
        :param ec2_tag_set: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.
        :param load_balancer_info: ``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.
        :param on_premises_instance_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.
        :param on_premises_tag_set: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.
        :param trigger_configurations: ``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.
        """
        props = CfnDeploymentGroupProps(application_name=application_name, service_role_arn=service_role_arn, alarm_configuration=alarm_configuration, auto_rollback_configuration=auto_rollback_configuration, auto_scaling_groups=auto_scaling_groups, deployment=deployment, deployment_config_name=deployment_config_name, deployment_group_name=deployment_group_name, deployment_style=deployment_style, ec2_tag_filters=ec2_tag_filters, ec2_tag_set=ec2_tag_set, load_balancer_info=load_balancer_info, on_premises_instance_tag_filters=on_premises_instance_tag_filters, on_premises_tag_set=on_premises_tag_set, trigger_configurations=trigger_configurations)

        jsii.create(CfnDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        """
        return jsii.get(self, "applicationName")

    @application_name.setter
    def application_name(self, value: str):
        return jsii.set(self, "applicationName", value)

    @property
    @jsii.member(jsii_name="serviceRoleArn")
    def service_role_arn(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        """
        return jsii.get(self, "serviceRoleArn")

    @service_role_arn.setter
    def service_role_arn(self, value: str):
        return jsii.set(self, "serviceRoleArn", value)

    @property
    @jsii.member(jsii_name="alarmConfiguration")
    def alarm_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AlarmConfigurationProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        """
        return jsii.get(self, "alarmConfiguration")

    @alarm_configuration.setter
    def alarm_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AlarmConfigurationProperty"]]]):
        return jsii.set(self, "alarmConfiguration", value)

    @property
    @jsii.member(jsii_name="autoRollbackConfiguration")
    def auto_rollback_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AutoRollbackConfigurationProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        """
        return jsii.get(self, "autoRollbackConfiguration")

    @auto_rollback_configuration.setter
    def auto_rollback_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["AutoRollbackConfigurationProperty"]]]):
        return jsii.set(self, "autoRollbackConfiguration", value)

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        """
        return jsii.get(self, "autoScalingGroups")

    @auto_scaling_groups.setter
    def auto_scaling_groups(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "autoScalingGroups", value)

    @property
    @jsii.member(jsii_name="deployment")
    def deployment(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Deployment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        """
        return jsii.get(self, "deployment")

    @deployment.setter
    def deployment(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentProperty"]]]):
        return jsii.set(self, "deployment", value)

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        """
        return jsii.get(self, "deploymentConfigName")

    @deployment_config_name.setter
    def deployment_config_name(self, value: typing.Optional[str]):
        return jsii.set(self, "deploymentConfigName", value)

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        """
        return jsii.get(self, "deploymentGroupName")

    @deployment_group_name.setter
    def deployment_group_name(self, value: typing.Optional[str]):
        return jsii.set(self, "deploymentGroupName", value)

    @property
    @jsii.member(jsii_name="deploymentStyle")
    def deployment_style(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentStyleProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        """
        return jsii.get(self, "deploymentStyle")

    @deployment_style.setter
    def deployment_style(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["DeploymentStyleProperty"]]]):
        return jsii.set(self, "deploymentStyle", value)

    @property
    @jsii.member(jsii_name="ec2TagFilters")
    def ec2_tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EC2TagFilterProperty"]]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        """
        return jsii.get(self, "ec2TagFilters")

    @ec2_tag_filters.setter
    def ec2_tag_filters(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "EC2TagFilterProperty"]]]]]):
        return jsii.set(self, "ec2TagFilters", value)

    @property
    @jsii.member(jsii_name="ec2TagSet")
    def ec2_tag_set(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EC2TagSetProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        """
        return jsii.get(self, "ec2TagSet")

    @ec2_tag_set.setter
    def ec2_tag_set(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["EC2TagSetProperty"]]]):
        return jsii.set(self, "ec2TagSet", value)

    @property
    @jsii.member(jsii_name="loadBalancerInfo")
    def load_balancer_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoadBalancerInfoProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        """
        return jsii.get(self, "loadBalancerInfo")

    @load_balancer_info.setter
    def load_balancer_info(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["LoadBalancerInfoProperty"]]]):
        return jsii.set(self, "loadBalancerInfo", value)

    @property
    @jsii.member(jsii_name="onPremisesInstanceTagFilters")
    def on_premises_instance_tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TagFilterProperty"]]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        """
        return jsii.get(self, "onPremisesInstanceTagFilters")

    @on_premises_instance_tag_filters.setter
    def on_premises_instance_tag_filters(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TagFilterProperty"]]]]]):
        return jsii.set(self, "onPremisesInstanceTagFilters", value)

    @property
    @jsii.member(jsii_name="onPremisesTagSet")
    def on_premises_tag_set(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["OnPremisesTagSetProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        """
        return jsii.get(self, "onPremisesTagSet")

    @on_premises_tag_set.setter
    def on_premises_tag_set(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["OnPremisesTagSetProperty"]]]):
        return jsii.set(self, "onPremisesTagSet", value)

    @property
    @jsii.member(jsii_name="triggerConfigurations")
    def trigger_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TriggerConfigProperty"]]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        """
        return jsii.get(self, "triggerConfigurations")

    @trigger_configurations.setter
    def trigger_configurations(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "TriggerConfigProperty"]]]]]):
        return jsii.set(self, "triggerConfigurations", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AlarmConfigurationProperty", jsii_struct_bases=[], name_mapping={'alarms': 'alarms', 'enabled': 'enabled', 'ignore_poll_alarm_failure': 'ignorePollAlarmFailure'})
    class AlarmConfigurationProperty():
        def __init__(self, *, alarms: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.AlarmProperty"]]]]]=None, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, ignore_poll_alarm_failure: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param alarms: ``CfnDeploymentGroup.AlarmConfigurationProperty.Alarms``.
            :param enabled: ``CfnDeploymentGroup.AlarmConfigurationProperty.Enabled``.
            :param ignore_poll_alarm_failure: ``CfnDeploymentGroup.AlarmConfigurationProperty.IgnorePollAlarmFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html
            """
            self._values = {
            }
            if alarms is not None: self._values["alarms"] = alarms
            if enabled is not None: self._values["enabled"] = enabled
            if ignore_poll_alarm_failure is not None: self._values["ignore_poll_alarm_failure"] = ignore_poll_alarm_failure

        @property
        def alarms(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.AlarmProperty"]]]]]:
            """``CfnDeploymentGroup.AlarmConfigurationProperty.Alarms``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-alarms
            """
            return self._values.get('alarms')

        @property
        def enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeploymentGroup.AlarmConfigurationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-enabled
            """
            return self._values.get('enabled')

        @property
        def ignore_poll_alarm_failure(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeploymentGroup.AlarmConfigurationProperty.IgnorePollAlarmFailure``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarmconfiguration.html#cfn-codedeploy-deploymentgroup-alarmconfiguration-ignorepollalarmfailure
            """
            return self._values.get('ignore_poll_alarm_failure')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AlarmConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AlarmProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class AlarmProperty():
        def __init__(self, *, name: typing.Optional[str]=None):
            """
            :param name: ``CfnDeploymentGroup.AlarmProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.AlarmProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-alarm.html#cfn-codedeploy-deploymentgroup-alarm-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AlarmProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.AutoRollbackConfigurationProperty", jsii_struct_bases=[], name_mapping={'enabled': 'enabled', 'events': 'events'})
    class AutoRollbackConfigurationProperty():
        def __init__(self, *, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, events: typing.Optional[typing.List[str]]=None):
            """
            :param enabled: ``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Enabled``.
            :param events: ``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html
            """
            self._values = {
            }
            if enabled is not None: self._values["enabled"] = enabled
            if events is not None: self._values["events"] = events

        @property
        def enabled(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Enabled``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-enabled
            """
            return self._values.get('enabled')

        @property
        def events(self) -> typing.Optional[typing.List[str]]:
            """``CfnDeploymentGroup.AutoRollbackConfigurationProperty.Events``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-autorollbackconfiguration.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration-events
            """
            return self._values.get('events')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'AutoRollbackConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentProperty", jsii_struct_bases=[], name_mapping={'revision': 'revision', 'description': 'description', 'ignore_application_stop_failures': 'ignoreApplicationStopFailures'})
    class DeploymentProperty():
        def __init__(self, *, revision: typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.RevisionLocationProperty"], description: typing.Optional[str]=None, ignore_application_stop_failures: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param revision: ``CfnDeploymentGroup.DeploymentProperty.Revision``.
            :param description: ``CfnDeploymentGroup.DeploymentProperty.Description``.
            :param ignore_application_stop_failures: ``CfnDeploymentGroup.DeploymentProperty.IgnoreApplicationStopFailures``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html
            """
            self._values = {
                'revision': revision,
            }
            if description is not None: self._values["description"] = description
            if ignore_application_stop_failures is not None: self._values["ignore_application_stop_failures"] = ignore_application_stop_failures

        @property
        def revision(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.RevisionLocationProperty"]:
            """``CfnDeploymentGroup.DeploymentProperty.Revision``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision
            """
            return self._values.get('revision')

        @property
        def description(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.DeploymentProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-description
            """
            return self._values.get('description')

        @property
        def ignore_application_stop_failures(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDeploymentGroup.DeploymentProperty.IgnoreApplicationStopFailures``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment.html#cfn-properties-codedeploy-deploymentgroup-deployment-ignoreapplicationstopfailures
            """
            return self._values.get('ignore_application_stop_failures')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.DeploymentStyleProperty", jsii_struct_bases=[], name_mapping={'deployment_option': 'deploymentOption', 'deployment_type': 'deploymentType'})
    class DeploymentStyleProperty():
        def __init__(self, *, deployment_option: typing.Optional[str]=None, deployment_type: typing.Optional[str]=None):
            """
            :param deployment_option: ``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentOption``.
            :param deployment_type: ``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html
            """
            self._values = {
            }
            if deployment_option is not None: self._values["deployment_option"] = deployment_option
            if deployment_type is not None: self._values["deployment_type"] = deployment_type

        @property
        def deployment_option(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentOption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymentoption
            """
            return self._values.get('deployment_option')

        @property
        def deployment_type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.DeploymentStyleProperty.DeploymentType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deploymentstyle.html#cfn-codedeploy-deploymentgroup-deploymentstyle-deploymenttype
            """
            return self._values.get('deployment_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DeploymentStyleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagFilterProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'type': 'type', 'value': 'value'})
    class EC2TagFilterProperty():
        def __init__(self, *, key: typing.Optional[str]=None, type: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param key: ``CfnDeploymentGroup.EC2TagFilterProperty.Key``.
            :param type: ``CfnDeploymentGroup.EC2TagFilterProperty.Type``.
            :param value: ``CfnDeploymentGroup.EC2TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if type is not None: self._values["type"] = type
            if value is not None: self._values["value"] = value

        @property
        def key(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.EC2TagFilterProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-key
            """
            return self._values.get('key')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.EC2TagFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-type
            """
            return self._values.get('type')

        @property
        def value(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.EC2TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagfilter.html#cfn-codedeploy-deploymentgroup-ec2tagfilter-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EC2TagFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagSetListObjectProperty", jsii_struct_bases=[], name_mapping={'ec2_tag_group': 'ec2TagGroup'})
    class EC2TagSetListObjectProperty():
        def __init__(self, *, ec2_tag_group: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]]]=None):
            """
            :param ec2_tag_group: ``CfnDeploymentGroup.EC2TagSetListObjectProperty.Ec2TagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html
            """
            self._values = {
            }
            if ec2_tag_group is not None: self._values["ec2_tag_group"] = ec2_tag_group

        @property
        def ec2_tag_group(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]]]:
            """``CfnDeploymentGroup.EC2TagSetListObjectProperty.Ec2TagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagsetlistobject.html#cfn-codedeploy-deploymentgroup-ec2tagsetlistobject-ec2taggroup
            """
            return self._values.get('ec2_tag_group')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EC2TagSetListObjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.EC2TagSetProperty", jsii_struct_bases=[], name_mapping={'ec2_tag_set_list': 'ec2TagSetList'})
    class EC2TagSetProperty():
        def __init__(self, *, ec2_tag_set_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.EC2TagSetListObjectProperty"]]]]]=None):
            """
            :param ec2_tag_set_list: ``CfnDeploymentGroup.EC2TagSetProperty.Ec2TagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html
            """
            self._values = {
            }
            if ec2_tag_set_list is not None: self._values["ec2_tag_set_list"] = ec2_tag_set_list

        @property
        def ec2_tag_set_list(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.EC2TagSetListObjectProperty"]]]]]:
            """``CfnDeploymentGroup.EC2TagSetProperty.Ec2TagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-ec2tagset.html#cfn-codedeploy-deploymentgroup-ec2tagset-ec2tagsetlist
            """
            return self._values.get('ec2_tag_set_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EC2TagSetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.ELBInfoProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class ELBInfoProperty():
        def __init__(self, *, name: typing.Optional[str]=None):
            """
            :param name: ``CfnDeploymentGroup.ELBInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.ELBInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-elbinfo.html#cfn-codedeploy-deploymentgroup-elbinfo-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ELBInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.GitHubLocationProperty", jsii_struct_bases=[], name_mapping={'commit_id': 'commitId', 'repository': 'repository'})
    class GitHubLocationProperty():
        def __init__(self, *, commit_id: str, repository: str):
            """
            :param commit_id: ``CfnDeploymentGroup.GitHubLocationProperty.CommitId``.
            :param repository: ``CfnDeploymentGroup.GitHubLocationProperty.Repository``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html
            """
            self._values = {
                'commit_id': commit_id,
                'repository': repository,
            }

        @property
        def commit_id(self) -> str:
            """``CfnDeploymentGroup.GitHubLocationProperty.CommitId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-commitid
            """
            return self._values.get('commit_id')

        @property
        def repository(self) -> str:
            """``CfnDeploymentGroup.GitHubLocationProperty.Repository``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-githublocation.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation-repository
            """
            return self._values.get('repository')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GitHubLocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.LoadBalancerInfoProperty", jsii_struct_bases=[], name_mapping={'elb_info_list': 'elbInfoList', 'target_group_info_list': 'targetGroupInfoList'})
    class LoadBalancerInfoProperty():
        def __init__(self, *, elb_info_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.ELBInfoProperty"]]]]]=None, target_group_info_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]]]=None):
            """
            :param elb_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.ElbInfoList``.
            :param target_group_info_list: ``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupInfoList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html
            """
            self._values = {
            }
            if elb_info_list is not None: self._values["elb_info_list"] = elb_info_list
            if target_group_info_list is not None: self._values["target_group_info_list"] = target_group_info_list

        @property
        def elb_info_list(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.ELBInfoProperty"]]]]]:
            """``CfnDeploymentGroup.LoadBalancerInfoProperty.ElbInfoList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-elbinfolist
            """
            return self._values.get('elb_info_list')

        @property
        def target_group_info_list(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TargetGroupInfoProperty"]]]]]:
            """``CfnDeploymentGroup.LoadBalancerInfoProperty.TargetGroupInfoList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-loadbalancerinfo.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo-targetgroupinfolist
            """
            return self._values.get('target_group_info_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'LoadBalancerInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.OnPremisesTagSetListObjectProperty", jsii_struct_bases=[], name_mapping={'on_premises_tag_group': 'onPremisesTagGroup'})
    class OnPremisesTagSetListObjectProperty():
        def __init__(self, *, on_premises_tag_group: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]]]=None):
            """
            :param on_premises_tag_group: ``CfnDeploymentGroup.OnPremisesTagSetListObjectProperty.OnPremisesTagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html
            """
            self._values = {
            }
            if on_premises_tag_group is not None: self._values["on_premises_tag_group"] = on_premises_tag_group

        @property
        def on_premises_tag_group(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]]]:
            """``CfnDeploymentGroup.OnPremisesTagSetListObjectProperty.OnPremisesTagGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagsetlistobject.html#cfn-codedeploy-deploymentgroup-onpremisestagsetlistobject-onpremisestaggroup
            """
            return self._values.get('on_premises_tag_group')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnPremisesTagSetListObjectProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.OnPremisesTagSetProperty", jsii_struct_bases=[], name_mapping={'on_premises_tag_set_list': 'onPremisesTagSetList'})
    class OnPremisesTagSetProperty():
        def __init__(self, *, on_premises_tag_set_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetListObjectProperty"]]]]]=None):
            """
            :param on_premises_tag_set_list: ``CfnDeploymentGroup.OnPremisesTagSetProperty.OnPremisesTagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html
            """
            self._values = {
            }
            if on_premises_tag_set_list is not None: self._values["on_premises_tag_set_list"] = on_premises_tag_set_list

        @property
        def on_premises_tag_set_list(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.OnPremisesTagSetListObjectProperty"]]]]]:
            """``CfnDeploymentGroup.OnPremisesTagSetProperty.OnPremisesTagSetList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-onpremisestagset.html#cfn-codedeploy-deploymentgroup-onpremisestagset-onpremisestagsetlist
            """
            return self._values.get('on_premises_tag_set_list')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OnPremisesTagSetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.RevisionLocationProperty", jsii_struct_bases=[], name_mapping={'git_hub_location': 'gitHubLocation', 'revision_type': 'revisionType', 's3_location': 's3Location'})
    class RevisionLocationProperty():
        def __init__(self, *, git_hub_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.GitHubLocationProperty"]]]=None, revision_type: typing.Optional[str]=None, s3_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.S3LocationProperty"]]]=None):
            """
            :param git_hub_location: ``CfnDeploymentGroup.RevisionLocationProperty.GitHubLocation``.
            :param revision_type: ``CfnDeploymentGroup.RevisionLocationProperty.RevisionType``.
            :param s3_location: ``CfnDeploymentGroup.RevisionLocationProperty.S3Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html
            """
            self._values = {
            }
            if git_hub_location is not None: self._values["git_hub_location"] = git_hub_location
            if revision_type is not None: self._values["revision_type"] = revision_type
            if s3_location is not None: self._values["s3_location"] = s3_location

        @property
        def git_hub_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.GitHubLocationProperty"]]]:
            """``CfnDeploymentGroup.RevisionLocationProperty.GitHubLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-githublocation
            """
            return self._values.get('git_hub_location')

        @property
        def revision_type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.RevisionLocationProperty.RevisionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-revisiontype
            """
            return self._values.get('revision_type')

        @property
        def s3_location(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.S3LocationProperty"]]]:
            """``CfnDeploymentGroup.RevisionLocationProperty.S3Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location
            """
            return self._values.get('s3_location')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'RevisionLocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.S3LocationProperty", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'key': 'key', 'bundle_type': 'bundleType', 'e_tag': 'eTag', 'version': 'version'})
    class S3LocationProperty():
        def __init__(self, *, bucket: str, key: str, bundle_type: typing.Optional[str]=None, e_tag: typing.Optional[str]=None, version: typing.Optional[str]=None):
            """
            :param bucket: ``CfnDeploymentGroup.S3LocationProperty.Bucket``.
            :param key: ``CfnDeploymentGroup.S3LocationProperty.Key``.
            :param bundle_type: ``CfnDeploymentGroup.S3LocationProperty.BundleType``.
            :param e_tag: ``CfnDeploymentGroup.S3LocationProperty.ETag``.
            :param version: ``CfnDeploymentGroup.S3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html
            """
            self._values = {
                'bucket': bucket,
                'key': key,
            }
            if bundle_type is not None: self._values["bundle_type"] = bundle_type
            if e_tag is not None: self._values["e_tag"] = e_tag
            if version is not None: self._values["version"] = version

        @property
        def bucket(self) -> str:
            """``CfnDeploymentGroup.S3LocationProperty.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bucket
            """
            return self._values.get('bucket')

        @property
        def key(self) -> str:
            """``CfnDeploymentGroup.S3LocationProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-key
            """
            return self._values.get('key')

        @property
        def bundle_type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.S3LocationProperty.BundleType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-bundletype
            """
            return self._values.get('bundle_type')

        @property
        def e_tag(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.S3LocationProperty.ETag``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-etag
            """
            return self._values.get('e_tag')

        @property
        def version(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.S3LocationProperty.Version``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-deployment-revision-s3location.html#cfn-properties-codedeploy-deploymentgroup-deployment-revision-s3location-value
            """
            return self._values.get('version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3LocationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TagFilterProperty", jsii_struct_bases=[], name_mapping={'key': 'key', 'type': 'type', 'value': 'value'})
    class TagFilterProperty():
        def __init__(self, *, key: typing.Optional[str]=None, type: typing.Optional[str]=None, value: typing.Optional[str]=None):
            """
            :param key: ``CfnDeploymentGroup.TagFilterProperty.Key``.
            :param type: ``CfnDeploymentGroup.TagFilterProperty.Type``.
            :param value: ``CfnDeploymentGroup.TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html
            """
            self._values = {
            }
            if key is not None: self._values["key"] = key
            if type is not None: self._values["type"] = type
            if value is not None: self._values["value"] = value

        @property
        def key(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TagFilterProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-key
            """
            return self._values.get('key')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TagFilterProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-type
            """
            return self._values.get('type')

        @property
        def value(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TagFilterProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-tagfilter.html#cfn-codedeploy-deploymentgroup-tagfilter-value
            """
            return self._values.get('value')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TagFilterProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TargetGroupInfoProperty", jsii_struct_bases=[], name_mapping={'name': 'name'})
    class TargetGroupInfoProperty():
        def __init__(self, *, name: typing.Optional[str]=None):
            """
            :param name: ``CfnDeploymentGroup.TargetGroupInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TargetGroupInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-targetgroupinfo.html#cfn-codedeploy-deploymentgroup-targetgroupinfo-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetGroupInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroup.TriggerConfigProperty", jsii_struct_bases=[], name_mapping={'trigger_events': 'triggerEvents', 'trigger_name': 'triggerName', 'trigger_target_arn': 'triggerTargetArn'})
    class TriggerConfigProperty():
        def __init__(self, *, trigger_events: typing.Optional[typing.List[str]]=None, trigger_name: typing.Optional[str]=None, trigger_target_arn: typing.Optional[str]=None):
            """
            :param trigger_events: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerEvents``.
            :param trigger_name: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerName``.
            :param trigger_target_arn: ``CfnDeploymentGroup.TriggerConfigProperty.TriggerTargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html
            """
            self._values = {
            }
            if trigger_events is not None: self._values["trigger_events"] = trigger_events
            if trigger_name is not None: self._values["trigger_name"] = trigger_name
            if trigger_target_arn is not None: self._values["trigger_target_arn"] = trigger_target_arn

        @property
        def trigger_events(self) -> typing.Optional[typing.List[str]]:
            """``CfnDeploymentGroup.TriggerConfigProperty.TriggerEvents``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggerevents
            """
            return self._values.get('trigger_events')

        @property
        def trigger_name(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TriggerConfigProperty.TriggerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggername
            """
            return self._values.get('trigger_name')

        @property
        def trigger_target_arn(self) -> typing.Optional[str]:
            """``CfnDeploymentGroup.TriggerConfigProperty.TriggerTargetArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codedeploy-deploymentgroup-triggerconfig.html#cfn-codedeploy-deploymentgroup-triggerconfig-triggertargetarn
            """
            return self._values.get('trigger_target_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TriggerConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.CfnDeploymentGroupProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName', 'service_role_arn': 'serviceRoleArn', 'alarm_configuration': 'alarmConfiguration', 'auto_rollback_configuration': 'autoRollbackConfiguration', 'auto_scaling_groups': 'autoScalingGroups', 'deployment': 'deployment', 'deployment_config_name': 'deploymentConfigName', 'deployment_group_name': 'deploymentGroupName', 'deployment_style': 'deploymentStyle', 'ec2_tag_filters': 'ec2TagFilters', 'ec2_tag_set': 'ec2TagSet', 'load_balancer_info': 'loadBalancerInfo', 'on_premises_instance_tag_filters': 'onPremisesInstanceTagFilters', 'on_premises_tag_set': 'onPremisesTagSet', 'trigger_configurations': 'triggerConfigurations'})
class CfnDeploymentGroupProps():
    def __init__(self, *, application_name: str, service_role_arn: str, alarm_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.AlarmConfigurationProperty"]]]=None, auto_rollback_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.AutoRollbackConfigurationProperty"]]]=None, auto_scaling_groups: typing.Optional[typing.List[str]]=None, deployment: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.DeploymentProperty"]]]=None, deployment_config_name: typing.Optional[str]=None, deployment_group_name: typing.Optional[str]=None, deployment_style: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.DeploymentStyleProperty"]]]=None, ec2_tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]]]=None, ec2_tag_set: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.EC2TagSetProperty"]]]=None, load_balancer_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.LoadBalancerInfoProperty"]]]=None, on_premises_instance_tag_filters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]]]=None, on_premises_tag_set: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.OnPremisesTagSetProperty"]]]=None, trigger_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TriggerConfigProperty"]]]]]=None):
        """Properties for defining a ``AWS::CodeDeploy::DeploymentGroup``.

        :param application_name: ``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.
        :param service_role_arn: ``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.
        :param alarm_configuration: ``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.
        :param auto_rollback_configuration: ``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.
        :param auto_scaling_groups: ``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.
        :param deployment: ``AWS::CodeDeploy::DeploymentGroup.Deployment``.
        :param deployment_config_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.
        :param deployment_group_name: ``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.
        :param deployment_style: ``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.
        :param ec2_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.
        :param ec2_tag_set: ``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.
        :param load_balancer_info: ``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.
        :param on_premises_instance_tag_filters: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.
        :param on_premises_tag_set: ``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.
        :param trigger_configurations: ``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html
        """
        self._values = {
            'application_name': application_name,
            'service_role_arn': service_role_arn,
        }
        if alarm_configuration is not None: self._values["alarm_configuration"] = alarm_configuration
        if auto_rollback_configuration is not None: self._values["auto_rollback_configuration"] = auto_rollback_configuration
        if auto_scaling_groups is not None: self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment is not None: self._values["deployment"] = deployment
        if deployment_config_name is not None: self._values["deployment_config_name"] = deployment_config_name
        if deployment_group_name is not None: self._values["deployment_group_name"] = deployment_group_name
        if deployment_style is not None: self._values["deployment_style"] = deployment_style
        if ec2_tag_filters is not None: self._values["ec2_tag_filters"] = ec2_tag_filters
        if ec2_tag_set is not None: self._values["ec2_tag_set"] = ec2_tag_set
        if load_balancer_info is not None: self._values["load_balancer_info"] = load_balancer_info
        if on_premises_instance_tag_filters is not None: self._values["on_premises_instance_tag_filters"] = on_premises_instance_tag_filters
        if on_premises_tag_set is not None: self._values["on_premises_tag_set"] = on_premises_tag_set
        if trigger_configurations is not None: self._values["trigger_configurations"] = trigger_configurations

    @property
    def application_name(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ApplicationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-applicationname
        """
        return self._values.get('application_name')

    @property
    def service_role_arn(self) -> str:
        """``AWS::CodeDeploy::DeploymentGroup.ServiceRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-servicerolearn
        """
        return self._values.get('service_role_arn')

    @property
    def alarm_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.AlarmConfigurationProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.AlarmConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-alarmconfiguration
        """
        return self._values.get('alarm_configuration')

    @property
    def auto_rollback_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.AutoRollbackConfigurationProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoRollbackConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autorollbackconfiguration
        """
        return self._values.get('auto_rollback_configuration')

    @property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::CodeDeploy::DeploymentGroup.AutoScalingGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-autoscalinggroups
        """
        return self._values.get('auto_scaling_groups')

    @property
    def deployment(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.DeploymentProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Deployment``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deployment
        """
        return self._values.get('deployment')

    @property
    def deployment_config_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentconfigname
        """
        return self._values.get('deployment_config_name')

    @property
    def deployment_group_name(self) -> typing.Optional[str]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentgroupname
        """
        return self._values.get('deployment_group_name')

    @property
    def deployment_style(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.DeploymentStyleProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.DeploymentStyle``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-deploymentstyle
        """
        return self._values.get('deployment_style')

    @property
    def ec2_tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.EC2TagFilterProperty"]]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagfilters
        """
        return self._values.get('ec2_tag_filters')

    @property
    def ec2_tag_set(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.EC2TagSetProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.Ec2TagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-ec2tagset
        """
        return self._values.get('ec2_tag_set')

    @property
    def load_balancer_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.LoadBalancerInfoProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.LoadBalancerInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-loadbalancerinfo
        """
        return self._values.get('load_balancer_info')

    @property
    def on_premises_instance_tag_filters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TagFilterProperty"]]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesInstanceTagFilters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisesinstancetagfilters
        """
        return self._values.get('on_premises_instance_tag_filters')

    @property
    def on_premises_tag_set(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDeploymentGroup.OnPremisesTagSetProperty"]]]:
        """``AWS::CodeDeploy::DeploymentGroup.OnPremisesTagSet``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-onpremisestagset
        """
        return self._values.get('on_premises_tag_set')

    @property
    def trigger_configurations(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnDeploymentGroup.TriggerConfigProperty"]]]]]:
        """``AWS::CodeDeploy::DeploymentGroup.TriggerConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codedeploy-deploymentgroup.html#cfn-codedeploy-deploymentgroup-triggerconfigurations
        """
        return self._values.get('trigger_configurations')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDeploymentGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.EcsApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName'})
class EcsApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None):
        """Construction properties for {@link EcsApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name

    @property
    def application_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Application.

        default
        :default: an auto-generated name will be used
        """
        return self._values.get('application_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcsDeploymentConfig(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.EcsDeploymentConfig"):
    """A custom Deployment Configuration for an ECS Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom ECS Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    resource:
    :resource:: AWS::CodeDeploy::DeploymentConfig
    """
    @jsii.member(jsii_name="fromEcsDeploymentConfigName")
    @classmethod
    def from_ecs_deployment_config_name(cls, _scope: aws_cdk.core.Construct, _id: str, ecs_deployment_config_name: str) -> "IEcsDeploymentConfig":
        """Import a custom Deployment Configuration for an ECS Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param ecs_deployment_config_name: the name of the referenced custom Deployment Configuration.

        return
        :return: a Construct representing a reference to an existing custom Deployment Configuration
        """
        return jsii.sinvoke(cls, "fromEcsDeploymentConfigName", [_scope, _id, ecs_deployment_config_name])

    @classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "IEcsDeploymentConfig":
        return jsii.sget(cls, "ALL_AT_ONCE")


class EcsDeploymentGroup(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.EcsDeploymentGroup"):
    """Note: This class currently stands as a namespaced container for importing an ECS Deployment Group defined outside the CDK app until CloudFormation supports provisioning ECS Deployment Groups.

    Until then it is closed (private constructor) and does not
    extend {@link cdk.Construct}.

    resource:
    :resource:: AWS::CodeDeploy::DeploymentGroup
    """
    @jsii.member(jsii_name="fromEcsDeploymentGroupAttributes")
    @classmethod
    def from_ecs_deployment_group_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, application: "IEcsApplication", deployment_group_name: str, deployment_config: typing.Optional["IEcsDeploymentConfig"]=None) -> "IEcsDeploymentGroup":
        """Import an ECS Deployment Group defined outside the CDK app.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param attrs: the properties of the referenced Deployment Group.
        :param application: The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        return
        :return: a Construct representing a reference to an existing Deployment Group
        """
        attrs = EcsDeploymentGroupAttributes(application=application, deployment_group_name=deployment_group_name, deployment_config=deployment_config)

        return jsii.sinvoke(cls, "fromEcsDeploymentGroupAttributes", [scope, id, attrs])


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.EcsDeploymentGroupAttributes", jsii_struct_bases=[], name_mapping={'application': 'application', 'deployment_group_name': 'deploymentGroupName', 'deployment_config': 'deploymentConfig'})
class EcsDeploymentGroupAttributes():
    def __init__(self, *, application: "IEcsApplication", deployment_group_name: str, deployment_config: typing.Optional["IEcsDeploymentConfig"]=None):
        """Properties of a reference to a CodeDeploy ECS Deployment Group.

        :param application: The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: EcsDeploymentConfig.ALL_AT_ONCE

        see
        :see: EcsDeploymentGroup#fromEcsDeploymentGroupAttributes
        """
        self._values = {
            'application': application,
            'deployment_group_name': deployment_group_name,
        }
        if deployment_config is not None: self._values["deployment_config"] = deployment_config

    @property
    def application(self) -> "IEcsApplication":
        """The reference to the CodeDeploy ECS Application that this Deployment Group belongs to."""
        return self._values.get('application')

    @property
    def deployment_group_name(self) -> str:
        """The physical, human-readable name of the CodeDeploy ECS Deployment Group that we are referencing."""
        return self._values.get('deployment_group_name')

    @property
    def deployment_config(self) -> typing.Optional["IEcsDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: EcsDeploymentConfig.ALL_AT_ONCE
        """
        return self._values.get('deployment_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsDeploymentGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IEcsApplication")
class IEcsApplication(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IEcsApplicationProxy

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _IEcsApplicationProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a reference to a CodeDeploy Application deploying to Amazon ECS.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link EcsApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link EcsApplication#fromEcsApplicationName} method.
    """
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IEcsApplication"
    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationName")


@jsii.implements(IEcsApplication)
class EcsApplication(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.EcsApplication"):
    """A CodeDeploy Application that deploys to an Amazon ECS service.

    resource:
    :resource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, application_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        """
        props = EcsApplicationProps(application_name=application_name)

        jsii.create(EcsApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromEcsApplicationName")
    @classmethod
    def from_ecs_application_name(cls, scope: aws_cdk.core.Construct, id: str, ecs_application_name: str) -> "IEcsApplication":
        """Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param ecs_application_name: the name of the application to import.

        return
        :return: a Construct representing a reference to an existing Application
        """
        return jsii.sinvoke(cls, "fromEcsApplicationName", [scope, id, ecs_application_name])

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IEcsDeploymentConfig")
class IEcsDeploymentConfig(jsii.compat.Protocol):
    """The Deployment Configuration of an ECS Deployment Group. The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IEcsDeploymentConfigProxy

    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        ...


class _IEcsDeploymentConfigProxy():
    """The Deployment Configuration of an ECS Deployment Group. The default, pre-defined Configurations are available as constants on the {@link EcsDeploymentConfig} class (for example, ``EcsDeploymentConfig.AllAtOnce``).

    Note: CloudFormation does not currently support creating custom ECS configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link EcsDeploymentConfig#fromEcsDeploymentConfigName}.
    """
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IEcsDeploymentConfig"
    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        return jsii.get(self, "deploymentConfigArn")

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        return jsii.get(self, "deploymentConfigName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IEcsDeploymentGroup")
class IEcsDeploymentGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Interface for an ECS deployment group."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IEcsDeploymentGroupProxy

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IEcsApplication":
        """The reference to the CodeDeploy ECS Application that this Deployment Group belongs to."""
        ...

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IEcsDeploymentConfig":
        """The Deployment Configuration this Group uses."""
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        attribute:
        :attribute:: true
        """
        ...


class _IEcsDeploymentGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Interface for an ECS deployment group."""
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IEcsDeploymentGroup"
    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IEcsApplication":
        """The reference to the CodeDeploy ECS Application that this Deployment Group belongs to."""
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IEcsDeploymentConfig":
        """The Deployment Configuration this Group uses."""
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaApplication")
class ILambdaApplication(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ILambdaApplicationProxy

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _ILambdaApplicationProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a reference to a CodeDeploy Application deploying to AWS Lambda.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link LambdaApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link LambdaApplication#fromLambdaApplicationName} method.
    """
    __jsii_type__ = "@aws-cdk/aws-codedeploy.ILambdaApplication"
    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaDeploymentConfig")
class ILambdaDeploymentConfig(jsii.compat.Protocol):
    """The Deployment Configuration of a Lambda Deployment Group. The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ILambdaDeploymentConfigProxy

    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        ...


class _ILambdaDeploymentConfigProxy():
    """The Deployment Configuration of a Lambda Deployment Group. The default, pre-defined Configurations are available as constants on the {@link LambdaDeploymentConfig} class (``LambdaDeploymentConfig.AllAtOnce``, ``LambdaDeploymentConfig.Canary10Percent30Minutes``, etc.).

    Note: CloudFormation does not currently support creating custom lambda configs outside
    of using a custom resource. You can import custom deployment config created outside the
    CDK or via a custom resource with {@link LambdaDeploymentConfig#import}.
    """
    __jsii_type__ = "@aws-cdk/aws-codedeploy.ILambdaDeploymentConfig"
    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        return jsii.get(self, "deploymentConfigArn")

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        return jsii.get(self, "deploymentConfigName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.ILambdaDeploymentGroup")
class ILambdaDeploymentGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Interface for a Lambda deployment groups."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILambdaDeploymentGroupProxy

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to."""
        ...

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "ILambdaDeploymentConfig":
        """The Deployment Configuration this Group uses."""
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        attribute:
        :attribute:: true
        """
        ...


class _ILambdaDeploymentGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Interface for a Lambda deployment groups."""
    __jsii_type__ = "@aws-cdk/aws-codedeploy.ILambdaDeploymentGroup"
    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to."""
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "ILambdaDeploymentConfig":
        """The Deployment Configuration this Group uses."""
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group.

        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerApplication")
class IServerApplication(aws_cdk.core.IResource, jsii.compat.Protocol):
    """Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IServerApplicationProxy

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _IServerApplicationProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """Represents a reference to a CodeDeploy Application deploying to EC2/on-premise instances.

    If you're managing the Application alongside the rest of your CDK resources,
    use the {@link ServerApplication} class.

    If you want to reference an already existing Application,
    or one defined in a different CDK Stack,
    use the {@link #fromServerApplicationName} method.
    """
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IServerApplication"
    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "applicationName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerDeploymentConfig")
class IServerDeploymentConfig(jsii.compat.Protocol):
    """The Deployment Configuration of an EC2/on-premise Deployment Group. The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class (``ServerDeploymentConfig.HalfAtATime``, ``ServerDeploymentConfig.AllAtOnce``, etc.). To create a custom Deployment Configuration, instantiate the {@link ServerDeploymentConfig} Construct."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IServerDeploymentConfigProxy

    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...


class _IServerDeploymentConfigProxy():
    """The Deployment Configuration of an EC2/on-premise Deployment Group. The default, pre-defined Configurations are available as constants on the {@link ServerDeploymentConfig} class (``ServerDeploymentConfig.HalfAtATime``, ``ServerDeploymentConfig.AllAtOnce``, etc.). To create a custom Deployment Configuration, instantiate the {@link ServerDeploymentConfig} Construct."""
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IServerDeploymentConfig"
    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentConfigArn")

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentConfigName")


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy.IServerDeploymentGroup")
class IServerDeploymentGroup(aws_cdk.core.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IServerDeploymentGroupProxy

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        ...

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        ...

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        ...


class _IServerDeploymentGroupProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    __jsii_type__ = "@aws-cdk/aws-codedeploy.IServerDeploymentGroup"
    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        return jsii.get(self, "autoScalingGroups")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


class InstanceTagSet(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.InstanceTagSet"):
    """Represents a set of instance tag groups. An instance will match a set if it matches all of the groups in the set - in other words, sets follow 'and' semantics. You can have a maximum of 3 tag groups inside a set."""
    def __init__(self, *instance_tag_groups: typing.Mapping[str,typing.List[str]]) -> None:
        """
        :param instance_tag_groups: -
        """
        jsii.create(InstanceTagSet, self, [*instance_tag_groups])

    @property
    @jsii.member(jsii_name="instanceTagGroups")
    def instance_tag_groups(self) -> typing.List[typing.Mapping[str,typing.List[str]]]:
        return jsii.get(self, "instanceTagGroups")


@jsii.implements(ILambdaApplication)
class LambdaApplication(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.LambdaApplication"):
    """A CodeDeploy Application that deploys to an AWS Lambda function.

    resource:
    :resource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, application_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        """
        props = LambdaApplicationProps(application_name=application_name)

        jsii.create(LambdaApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaApplicationName")
    @classmethod
    def from_lambda_application_name(cls, scope: aws_cdk.core.Construct, id: str, lambda_application_name: str) -> "ILambdaApplication":
        """Import an Application defined either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param lambda_application_name: the name of the application to import.

        return
        :return: a Construct representing a reference to an existing Application
        """
        return jsii.sinvoke(cls, "fromLambdaApplicationName", [scope, id, lambda_application_name])

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName'})
class LambdaApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None):
        """Construction properties for {@link LambdaApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name

    @property
    def application_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Application.

        default
        :default: an auto-generated name will be used
        """
        return self._values.get('application_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LambdaDeploymentConfig(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentConfig"):
    """A custom Deployment Configuration for a Lambda Deployment Group.

    Note: This class currently stands as namespaced container of the default configurations
    until CloudFormation supports custom Lambda Deployment Configs. Until then it is closed
    (private constructor) and does not extend {@link cdk.Construct}

    resource:
    :resource:: AWS::CodeDeploy::DeploymentConfig
    """
    @jsii.member(jsii_name="import")
    @classmethod
    def import_(cls, _scope: aws_cdk.core.Construct, _id: str, *, deployment_config_name: str) -> "ILambdaDeploymentConfig":
        """Import a custom Deployment Configuration for a Lambda Deployment Group defined outside the CDK.

        :param _scope: the parent Construct for this new Construct.
        :param _id: the logical ID of this new Construct.
        :param props: the properties of the referenced custom Deployment Configuration.
        :param deployment_config_name: The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        return
        :return: a Construct representing a reference to an existing custom Deployment Configuration
        """
        props = LambdaDeploymentConfigImportProps(deployment_config_name=deployment_config_name)

        return jsii.sinvoke(cls, "import", [_scope, _id, props])

    @classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "ALL_AT_ONCE")

    @classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_10MINUTES")
    def CANARY_10_PERCENT_10_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "CANARY_10PERCENT_10MINUTES")

    @classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_15MINUTES")
    def CANARY_10_PERCENT_15_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "CANARY_10PERCENT_15MINUTES")

    @classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_30MINUTES")
    def CANARY_10_PERCENT_30_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "CANARY_10PERCENT_30MINUTES")

    @classproperty
    @jsii.member(jsii_name="CANARY_10PERCENT_5MINUTES")
    def CANARY_10_PERCENT_5_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "CANARY_10PERCENT_5MINUTES")

    @classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_10MINUTES")
    def LINEAR_10_PERCENT_EVERY_10_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_10MINUTES")

    @classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_1MINUTE")
    def LINEAR_10_PERCENT_EVERY_1_MINUTE(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_1MINUTE")

    @classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_2MINUTES")
    def LINEAR_10_PERCENT_EVERY_2_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_2MINUTES")

    @classproperty
    @jsii.member(jsii_name="LINEAR_10PERCENT_EVERY_3MINUTES")
    def LINEAR_10_PERCENT_EVERY_3_MINUTES(cls) -> "ILambdaDeploymentConfig":
        return jsii.sget(cls, "LINEAR_10PERCENT_EVERY_3MINUTES")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentConfigImportProps", jsii_struct_bases=[], name_mapping={'deployment_config_name': 'deploymentConfigName'})
class LambdaDeploymentConfigImportProps():
    def __init__(self, *, deployment_config_name: str):
        """Properties of a reference to a CodeDeploy Lambda Deployment Configuration.

        :param deployment_config_name: The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing.

        see
        :see: LambdaDeploymentConfig#import
        """
        self._values = {
            'deployment_config_name': deployment_config_name,
        }

    @property
    def deployment_config_name(self) -> str:
        """The physical, human-readable name of the custom CodeDeploy Lambda Deployment Configuration that we are referencing."""
        return self._values.get('deployment_config_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDeploymentConfigImportProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(ILambdaDeploymentGroup)
class LambdaDeploymentGroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroup"):
    """
    resource:
    :resource:: AWS::CodeDeploy::DeploymentGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, alias: aws_cdk.aws_lambda.Alias, alarms: typing.Optional[typing.List[aws_cdk.aws_cloudwatch.IAlarm]]=None, application: typing.Optional["ILambdaApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, post_hook: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, pre_hook: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param alias: Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: The Lambda function to run before traffic routing starts. Default: - None.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.
        """
        props = LambdaDeploymentGroupProps(alias=alias, alarms=alarms, application=application, auto_rollback=auto_rollback, deployment_config=deployment_config, deployment_group_name=deployment_group_name, ignore_poll_alarms_failure=ignore_poll_alarms_failure, post_hook=post_hook, pre_hook=pre_hook, role=role)

        jsii.create(LambdaDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromLambdaDeploymentGroupAttributes")
    @classmethod
    def from_lambda_deployment_group_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, application: "ILambdaApplication", deployment_group_name: str, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None) -> "ILambdaDeploymentGroup":
        """Import an Lambda Deployment Group defined either outside the CDK app, or in a different AWS region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param attrs: the properties of the referenced Deployment Group.
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        return
        :return: a Construct representing a reference to an existing Deployment Group
        """
        attrs = LambdaDeploymentGroupAttributes(application=application, deployment_group_name=deployment_group_name, deployment_config=deployment_config)

        return jsii.sinvoke(cls, "fromLambdaDeploymentGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.IAlarm) -> None:
        """Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.
        """
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addPostHook")
    def add_post_hook(self, post_hook: aws_cdk.aws_lambda.IFunction) -> None:
        """Associate a function to run after deployment completes.

        :param post_hook: function to run after deployment completes.

        throws:
        :throws:: an error if a post-hook function is already configured
        """
        return jsii.invoke(self, "addPostHook", [post_hook])

    @jsii.member(jsii_name="addPreHook")
    def add_pre_hook(self, pre_hook: aws_cdk.aws_lambda.IFunction) -> None:
        """Associate a function to run before deployment begins.

        :param pre_hook: function to run before deployment beings.

        throws:
        :throws:: an error if a pre-hook function is already configured
        """
        return jsii.invoke(self, "addPreHook", [pre_hook])

    @jsii.member(jsii_name="grantPutLifecycleEventHookExecutionStatus")
    def grant_put_lifecycle_event_hook_execution_status(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant a principal permission to codedeploy:PutLifecycleEventHookExecutionStatus on this deployment group resource.

        :param grantee: to grant permission to.
        """
        return jsii.invoke(self, "grantPutLifecycleEventHookExecutionStatus", [grantee])

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to."""
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "ILambdaDeploymentConfig":
        """The Deployment Configuration this Group uses."""
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        """The ARN of this Deployment Group."""
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        """The physical name of the CodeDeploy Deployment Group."""
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroupAttributes", jsii_struct_bases=[], name_mapping={'application': 'application', 'deployment_group_name': 'deploymentGroupName', 'deployment_config': 'deploymentConfig'})
class LambdaDeploymentGroupAttributes():
    def __init__(self, *, application: "ILambdaApplication", deployment_group_name: str, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None):
        """Properties of a reference to a CodeDeploy Lambda Deployment Group.

        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES

        see
        :see: LambdaDeploymentGroup#fromLambdaDeploymentGroupAttributes
        """
        self._values = {
            'application': application,
            'deployment_group_name': deployment_group_name,
        }
        if deployment_config is not None: self._values["deployment_config"] = deployment_config

    @property
    def application(self) -> "ILambdaApplication":
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to."""
        return self._values.get('application')

    @property
    def deployment_group_name(self) -> str:
        """The physical, human-readable name of the CodeDeploy Lambda Deployment Group that we are referencing."""
        return self._values.get('deployment_group_name')

    @property
    def deployment_config(self) -> typing.Optional["ILambdaDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        """
        return self._values.get('deployment_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDeploymentGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.LambdaDeploymentGroupProps", jsii_struct_bases=[], name_mapping={'alias': 'alias', 'alarms': 'alarms', 'application': 'application', 'auto_rollback': 'autoRollback', 'deployment_config': 'deploymentConfig', 'deployment_group_name': 'deploymentGroupName', 'ignore_poll_alarms_failure': 'ignorePollAlarmsFailure', 'post_hook': 'postHook', 'pre_hook': 'preHook', 'role': 'role'})
class LambdaDeploymentGroupProps():
    def __init__(self, *, alias: aws_cdk.aws_lambda.Alias, alarms: typing.Optional[typing.List[aws_cdk.aws_cloudwatch.IAlarm]]=None, application: typing.Optional["ILambdaApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, deployment_config: typing.Optional["ILambdaDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, post_hook: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, pre_hook: typing.Optional[aws_cdk.aws_lambda.IFunction]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Construction properties for {@link LambdaDeploymentGroup}.

        :param alias: Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment. [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to. Default: - One will be created for you.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param post_hook: The Lambda function to run after traffic routing starts. Default: - None.
        :param pre_hook: The Lambda function to run before traffic routing starts. Default: - None.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.
        """
        if isinstance(auto_rollback, dict): auto_rollback = AutoRollbackConfig(**auto_rollback)
        self._values = {
            'alias': alias,
        }
        if alarms is not None: self._values["alarms"] = alarms
        if application is not None: self._values["application"] = application
        if auto_rollback is not None: self._values["auto_rollback"] = auto_rollback
        if deployment_config is not None: self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None: self._values["deployment_group_name"] = deployment_group_name
        if ignore_poll_alarms_failure is not None: self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if post_hook is not None: self._values["post_hook"] = post_hook
        if pre_hook is not None: self._values["pre_hook"] = pre_hook
        if role is not None: self._values["role"] = role

    @property
    def alias(self) -> aws_cdk.aws_lambda.Alias:
        """Lambda Alias to shift traffic. Updating the version of the alias will trigger a CodeDeploy deployment.

        [disable-awslint:ref-via-interface] since we need to modify the alias CFN resource update policy
        """
        return self._values.get('alias')

    @property
    def alarms(self) -> typing.Optional[typing.List[aws_cdk.aws_cloudwatch.IAlarm]]:
        """The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        default
        :default: []

        see
        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        """
        return self._values.get('alarms')

    @property
    def application(self) -> typing.Optional["ILambdaApplication"]:
        """The reference to the CodeDeploy Lambda Application that this Deployment Group belongs to.

        default
        :default: - One will be created for you.
        """
        return self._values.get('application')

    @property
    def auto_rollback(self) -> typing.Optional["AutoRollbackConfig"]:
        """The auto-rollback configuration for this Deployment Group.

        default
        :default: - default AutoRollbackConfig.
        """
        return self._values.get('auto_rollback')

    @property
    def deployment_config(self) -> typing.Optional["ILambdaDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: LambdaDeploymentConfig.CANARY_10PERCENT_5MINUTES
        """
        return self._values.get('deployment_config')

    @property
    def deployment_group_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Deployment Group.

        default
        :default: - An auto-generated name will be used.
        """
        return self._values.get('deployment_group_name')

    @property
    def ignore_poll_alarms_failure(self) -> typing.Optional[bool]:
        """Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        default
        :default: false
        """
        return self._values.get('ignore_poll_alarms_failure')

    @property
    def post_hook(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """The Lambda function to run after traffic routing starts.

        default
        :default: - None.
        """
        return self._values.get('post_hook')

    @property
    def pre_hook(self) -> typing.Optional[aws_cdk.aws_lambda.IFunction]:
        """The Lambda function to run before traffic routing starts.

        default
        :default: - None.
        """
        return self._values.get('pre_hook')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The service Role of this Deployment Group.

        default
        :default: - A new Role will be created.
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaDeploymentGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LoadBalancer(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codedeploy.LoadBalancer"):
    """An interface of an abstract load balancer, as needed by CodeDeploy. Create instances using the static factory methods: {@link #classic}, {@link #application} and {@link #network}."""
    @staticmethod
    def __jsii_proxy_class__():
        return _LoadBalancerProxy

    def __init__(self) -> None:
        jsii.create(LoadBalancer, self, [])

    @jsii.member(jsii_name="application")
    @classmethod
    def application(cls, alb_target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup) -> "LoadBalancer":
        """Creates a new CodeDeploy load balancer from an Application Load Balancer Target Group.

        :param alb_target_group: an ALB Target Group.
        """
        return jsii.sinvoke(cls, "application", [alb_target_group])

    @jsii.member(jsii_name="classic")
    @classmethod
    def classic(cls, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> "LoadBalancer":
        """Creates a new CodeDeploy load balancer from a Classic ELB Load Balancer.

        :param load_balancer: a classic ELB Load Balancer.
        """
        return jsii.sinvoke(cls, "classic", [load_balancer])

    @jsii.member(jsii_name="network")
    @classmethod
    def network(cls, nlb_target_group: aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup) -> "LoadBalancer":
        """Creates a new CodeDeploy load balancer from a Network Load Balancer Target Group.

        :param nlb_target_group: an NLB Target Group.
        """
        return jsii.sinvoke(cls, "network", [nlb_target_group])

    @property
    @jsii.member(jsii_name="generation")
    @abc.abstractmethod
    def generation(self) -> "LoadBalancerGeneration":
        ...

    @property
    @jsii.member(jsii_name="name")
    @abc.abstractmethod
    def name(self) -> str:
        ...


class _LoadBalancerProxy(LoadBalancer):
    @property
    @jsii.member(jsii_name="generation")
    def generation(self) -> "LoadBalancerGeneration":
        return jsii.get(self, "generation")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")


@jsii.enum(jsii_type="@aws-cdk/aws-codedeploy.LoadBalancerGeneration")
class LoadBalancerGeneration(enum.Enum):
    """The generations of AWS load balancing solutions."""
    FIRST = "FIRST"
    """The first generation (ELB Classic)."""
    SECOND = "SECOND"
    """The second generation (ALB and NLB)."""

class MinimumHealthyHosts(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.MinimumHealthyHosts"):
    """Minimum number of healthy hosts for a server deployment."""
    @jsii.member(jsii_name="count")
    @classmethod
    def count(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        """The minimum healhty hosts threshold expressed as an absolute number.

        :param value: -
        """
        return jsii.sinvoke(cls, "count", [value])

    @jsii.member(jsii_name="percentage")
    @classmethod
    def percentage(cls, value: jsii.Number) -> "MinimumHealthyHosts":
        """The minmum healhty hosts threshold expressed as a percentage of the fleet.

        :param value: -
        """
        return jsii.sinvoke(cls, "percentage", [value])


@jsii.implements(IServerApplication)
class ServerApplication(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.ServerApplication"):
    """A CodeDeploy Application that deploys to EC2/on-premise instances.

    resource:
    :resource:: AWS::CodeDeploy::Application
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, application_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        """
        props = ServerApplicationProps(application_name=application_name)

        jsii.create(ServerApplication, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerApplicationName")
    @classmethod
    def from_server_application_name(cls, scope: aws_cdk.core.Construct, id: str, server_application_name: str) -> "IServerApplication":
        """Import an Application defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_application_name: the name of the application to import.

        return
        :return: a Construct representing a reference to an existing Application
        """
        return jsii.sinvoke(cls, "fromServerApplicationName", [scope, id, server_application_name])

    @property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> str:
        return jsii.get(self, "applicationArn")

    @property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> str:
        return jsii.get(self, "applicationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerApplicationProps", jsii_struct_bases=[], name_mapping={'application_name': 'applicationName'})
class ServerApplicationProps():
    def __init__(self, *, application_name: typing.Optional[str]=None):
        """Construction properties for {@link ServerApplication}.

        :param application_name: The physical, human-readable name of the CodeDeploy Application. Default: an auto-generated name will be used
        """
        self._values = {
        }
        if application_name is not None: self._values["application_name"] = application_name

    @property
    def application_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Application.

        default
        :default: an auto-generated name will be used
        """
        return self._values.get('application_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerApplicationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IServerDeploymentConfig)
class ServerDeploymentConfig(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfig"):
    """A custom Deployment Configuration for an EC2/on-premise Deployment Group.

    resource:
    :resource:: AWS::CodeDeploy::DeploymentConfig
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, minimum_healthy_hosts: "MinimumHealthyHosts", deployment_config_name: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param minimum_healthy_hosts: Minimum number of healthy hosts.
        :param deployment_config_name: The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated
        """
        props = ServerDeploymentConfigProps(minimum_healthy_hosts=minimum_healthy_hosts, deployment_config_name=deployment_config_name)

        jsii.create(ServerDeploymentConfig, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentConfigName")
    @classmethod
    def from_server_deployment_config_name(cls, scope: aws_cdk.core.Construct, id: str, server_deployment_config_name: str) -> "IServerDeploymentConfig":
        """Import a custom Deployment Configuration for an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param server_deployment_config_name: the properties of the referenced custom Deployment Configuration.

        return
        :return: a Construct representing a reference to an existing custom Deployment Configuration
        """
        return jsii.sinvoke(cls, "fromServerDeploymentConfigName", [scope, id, server_deployment_config_name])

    @classproperty
    @jsii.member(jsii_name="ALL_AT_ONCE")
    def ALL_AT_ONCE(cls) -> "IServerDeploymentConfig":
        return jsii.sget(cls, "ALL_AT_ONCE")

    @classproperty
    @jsii.member(jsii_name="HALF_AT_A_TIME")
    def HALF_AT_A_TIME(cls) -> "IServerDeploymentConfig":
        return jsii.sget(cls, "HALF_AT_A_TIME")

    @classproperty
    @jsii.member(jsii_name="ONE_AT_A_TIME")
    def ONE_AT_A_TIME(cls) -> "IServerDeploymentConfig":
        return jsii.sget(cls, "ONE_AT_A_TIME")

    @property
    @jsii.member(jsii_name="deploymentConfigArn")
    def deployment_config_arn(self) -> str:
        return jsii.get(self, "deploymentConfigArn")

    @property
    @jsii.member(jsii_name="deploymentConfigName")
    def deployment_config_name(self) -> str:
        return jsii.get(self, "deploymentConfigName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentConfigProps", jsii_struct_bases=[], name_mapping={'minimum_healthy_hosts': 'minimumHealthyHosts', 'deployment_config_name': 'deploymentConfigName'})
class ServerDeploymentConfigProps():
    def __init__(self, *, minimum_healthy_hosts: "MinimumHealthyHosts", deployment_config_name: typing.Optional[str]=None):
        """Construction properties of {@link ServerDeploymentConfig}.

        :param minimum_healthy_hosts: Minimum number of healthy hosts.
        :param deployment_config_name: The physical, human-readable name of the Deployment Configuration. Default: a name will be auto-generated
        """
        self._values = {
            'minimum_healthy_hosts': minimum_healthy_hosts,
        }
        if deployment_config_name is not None: self._values["deployment_config_name"] = deployment_config_name

    @property
    def minimum_healthy_hosts(self) -> "MinimumHealthyHosts":
        """Minimum number of healthy hosts."""
        return self._values.get('minimum_healthy_hosts')

    @property
    def deployment_config_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the Deployment Configuration.

        default
        :default: a name will be auto-generated
        """
        return self._values.get('deployment_config_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerDeploymentConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(IServerDeploymentGroup)
class ServerDeploymentGroup(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroup"):
    """A CodeDeploy Deployment Group that deploys to EC2/on-premise instances.

    resource:
    :resource:: AWS::CodeDeploy::DeploymentGroup
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, alarms: typing.Optional[typing.List[aws_cdk.aws_cloudwatch.IAlarm]]=None, application: typing.Optional["IServerApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, auto_scaling_groups: typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]=None, deployment_config: typing.Optional["IServerDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ec2_instance_tags: typing.Optional["InstanceTagSet"]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, install_agent: typing.Optional[bool]=None, load_balancer: typing.Optional["LoadBalancer"]=None, on_premise_instance_tags: typing.Optional["InstanceTagSet"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.
        """
        props = ServerDeploymentGroupProps(alarms=alarms, application=application, auto_rollback=auto_rollback, auto_scaling_groups=auto_scaling_groups, deployment_config=deployment_config, deployment_group_name=deployment_group_name, ec2_instance_tags=ec2_instance_tags, ignore_poll_alarms_failure=ignore_poll_alarms_failure, install_agent=install_agent, load_balancer=load_balancer, on_premise_instance_tags=on_premise_instance_tags, role=role)

        jsii.create(ServerDeploymentGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromServerDeploymentGroupAttributes")
    @classmethod
    def from_server_deployment_group_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, application: "IServerApplication", deployment_group_name: str, deployment_config: typing.Optional["IServerDeploymentConfig"]=None) -> "IServerDeploymentGroup":
        """Import an EC2/on-premise Deployment Group defined either outside the CDK app, or in a different region.

        :param scope: the parent Construct for this new Construct.
        :param id: the logical ID of this new Construct.
        :param attrs: the properties of the referenced Deployment Group.
        :param application: The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        return
        :return: a Construct representing a reference to an existing Deployment Group
        """
        attrs = ServerDeploymentGroupAttributes(application=application, deployment_group_name=deployment_group_name, deployment_config=deployment_config)

        return jsii.sinvoke(cls, "fromServerDeploymentGroupAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAlarm")
    def add_alarm(self, alarm: aws_cdk.aws_cloudwatch.IAlarm) -> None:
        """Associates an additional alarm with this Deployment Group.

        :param alarm: the alarm to associate with this Deployment Group.
        """
        return jsii.invoke(self, "addAlarm", [alarm])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(self, asg: aws_cdk.aws_autoscaling.AutoScalingGroup) -> None:
        """Adds an additional auto-scaling group to this Deployment Group.

        :param asg: the auto-scaling group to add to this Deployment Group. [disable-awslint:ref-via-interface] is needed in order to install the code deploy agent by updating the ASGs user data.
        """
        return jsii.invoke(self, "addAutoScalingGroup", [asg])

    @property
    @jsii.member(jsii_name="application")
    def application(self) -> "IServerApplication":
        return jsii.get(self, "application")

    @property
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> "IServerDeploymentConfig":
        return jsii.get(self, "deploymentConfig")

    @property
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> str:
        return jsii.get(self, "deploymentGroupArn")

    @property
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> str:
        return jsii.get(self, "deploymentGroupName")

    @property
    @jsii.member(jsii_name="autoScalingGroups")
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        return jsii.get(self, "autoScalingGroups")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupAttributes", jsii_struct_bases=[], name_mapping={'application': 'application', 'deployment_group_name': 'deploymentGroupName', 'deployment_config': 'deploymentConfig'})
class ServerDeploymentGroupAttributes():
    def __init__(self, *, application: "IServerApplication", deployment_group_name: str, deployment_config: typing.Optional["IServerDeploymentConfig"]=None):
        """Properties of a reference to a CodeDeploy EC2/on-premise Deployment Group.

        :param application: The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to.
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing.
        :param deployment_config: The Deployment Configuration this Deployment Group uses. Default: ServerDeploymentConfig#OneAtATime

        see
        :see: ServerDeploymentGroup#import
        """
        self._values = {
            'application': application,
            'deployment_group_name': deployment_group_name,
        }
        if deployment_config is not None: self._values["deployment_config"] = deployment_config

    @property
    def application(self) -> "IServerApplication":
        """The reference to the CodeDeploy EC2/on-premise Application that this Deployment Group belongs to."""
        return self._values.get('application')

    @property
    def deployment_group_name(self) -> str:
        """The physical, human-readable name of the CodeDeploy EC2/on-premise Deployment Group that we are referencing."""
        return self._values.get('deployment_group_name')

    @property
    def deployment_config(self) -> typing.Optional["IServerDeploymentConfig"]:
        """The Deployment Configuration this Deployment Group uses.

        default
        :default: ServerDeploymentConfig#OneAtATime
        """
        return self._values.get('deployment_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerDeploymentGroupAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codedeploy.ServerDeploymentGroupProps", jsii_struct_bases=[], name_mapping={'alarms': 'alarms', 'application': 'application', 'auto_rollback': 'autoRollback', 'auto_scaling_groups': 'autoScalingGroups', 'deployment_config': 'deploymentConfig', 'deployment_group_name': 'deploymentGroupName', 'ec2_instance_tags': 'ec2InstanceTags', 'ignore_poll_alarms_failure': 'ignorePollAlarmsFailure', 'install_agent': 'installAgent', 'load_balancer': 'loadBalancer', 'on_premise_instance_tags': 'onPremiseInstanceTags', 'role': 'role'})
class ServerDeploymentGroupProps():
    def __init__(self, *, alarms: typing.Optional[typing.List[aws_cdk.aws_cloudwatch.IAlarm]]=None, application: typing.Optional["IServerApplication"]=None, auto_rollback: typing.Optional["AutoRollbackConfig"]=None, auto_scaling_groups: typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]=None, deployment_config: typing.Optional["IServerDeploymentConfig"]=None, deployment_group_name: typing.Optional[str]=None, ec2_instance_tags: typing.Optional["InstanceTagSet"]=None, ignore_poll_alarms_failure: typing.Optional[bool]=None, install_agent: typing.Optional[bool]=None, load_balancer: typing.Optional["LoadBalancer"]=None, on_premise_instance_tags: typing.Optional["InstanceTagSet"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Construction properties for {@link ServerDeploymentGroup}.

        :param alarms: The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger. Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method. Default: []
        :param application: The CodeDeploy EC2/on-premise Application this Deployment Group belongs to. Default: - A new Application will be created.
        :param auto_rollback: The auto-rollback configuration for this Deployment Group. Default: - default AutoRollbackConfig.
        :param auto_scaling_groups: The auto-scaling groups belonging to this Deployment Group. Auto-scaling groups can also be added after the Deployment Group is created using the {@link #addAutoScalingGroup} method. [disable-awslint:ref-via-interface] is needed because we update userdata for ASGs to install the codedeploy agent. Default: []
        :param deployment_config: The EC2/on-premise Deployment Configuration to use for this Deployment Group. Default: ServerDeploymentConfig#OneAtATime
        :param deployment_group_name: The physical, human-readable name of the CodeDeploy Deployment Group. Default: - An auto-generated name will be used.
        :param ec2_instance_tags: All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional EC2 instances will be added to the Deployment Group.
        :param ignore_poll_alarms_failure: Whether to continue a deployment even if fetching the alarm status from CloudWatch failed. Default: false
        :param install_agent: If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances. Default: true
        :param load_balancer: The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group. Default: - Deployment Group will not have a load balancer defined.
        :param on_premise_instance_tags: All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group. Default: - No additional on-premise instances will be added to the Deployment Group.
        :param role: The service Role of this Deployment Group. Default: - A new Role will be created.
        """
        if isinstance(auto_rollback, dict): auto_rollback = AutoRollbackConfig(**auto_rollback)
        self._values = {
        }
        if alarms is not None: self._values["alarms"] = alarms
        if application is not None: self._values["application"] = application
        if auto_rollback is not None: self._values["auto_rollback"] = auto_rollback
        if auto_scaling_groups is not None: self._values["auto_scaling_groups"] = auto_scaling_groups
        if deployment_config is not None: self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None: self._values["deployment_group_name"] = deployment_group_name
        if ec2_instance_tags is not None: self._values["ec2_instance_tags"] = ec2_instance_tags
        if ignore_poll_alarms_failure is not None: self._values["ignore_poll_alarms_failure"] = ignore_poll_alarms_failure
        if install_agent is not None: self._values["install_agent"] = install_agent
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if on_premise_instance_tags is not None: self._values["on_premise_instance_tags"] = on_premise_instance_tags
        if role is not None: self._values["role"] = role

    @property
    def alarms(self) -> typing.Optional[typing.List[aws_cdk.aws_cloudwatch.IAlarm]]:
        """The CloudWatch alarms associated with this Deployment Group. CodeDeploy will stop (and optionally roll back) a deployment if during it any of the alarms trigger.

        Alarms can also be added after the Deployment Group is created using the {@link #addAlarm} method.

        default
        :default: []

        see
        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/monitoring-create-alarms.html
        """
        return self._values.get('alarms')

    @property
    def application(self) -> typing.Optional["IServerApplication"]:
        """The CodeDeploy EC2/on-premise Application this Deployment Group belongs to.

        default
        :default: - A new Application will be created.
        """
        return self._values.get('application')

    @property
    def auto_rollback(self) -> typing.Optional["AutoRollbackConfig"]:
        """The auto-rollback configuration for this Deployment Group.

        default
        :default: - default AutoRollbackConfig.
        """
        return self._values.get('auto_rollback')

    @property
    def auto_scaling_groups(self) -> typing.Optional[typing.List[aws_cdk.aws_autoscaling.AutoScalingGroup]]:
        """The auto-scaling groups belonging to this Deployment Group.

        Auto-scaling groups can also be added after the Deployment Group is created
        using the {@link #addAutoScalingGroup} method.

        [disable-awslint:ref-via-interface] is needed because we update userdata
        for ASGs to install the codedeploy agent.

        default
        :default: []
        """
        return self._values.get('auto_scaling_groups')

    @property
    def deployment_config(self) -> typing.Optional["IServerDeploymentConfig"]:
        """The EC2/on-premise Deployment Configuration to use for this Deployment Group.

        default
        :default: ServerDeploymentConfig#OneAtATime
        """
        return self._values.get('deployment_config')

    @property
    def deployment_group_name(self) -> typing.Optional[str]:
        """The physical, human-readable name of the CodeDeploy Deployment Group.

        default
        :default: - An auto-generated name will be used.
        """
        return self._values.get('deployment_group_name')

    @property
    def ec2_instance_tags(self) -> typing.Optional["InstanceTagSet"]:
        """All EC2 instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        default
        :default: - No additional EC2 instances will be added to the Deployment Group.
        """
        return self._values.get('ec2_instance_tags')

    @property
    def ignore_poll_alarms_failure(self) -> typing.Optional[bool]:
        """Whether to continue a deployment even if fetching the alarm status from CloudWatch failed.

        default
        :default: false
        """
        return self._values.get('ignore_poll_alarms_failure')

    @property
    def install_agent(self) -> typing.Optional[bool]:
        """If you've provided any auto-scaling groups with the {@link #autoScalingGroups} property, you can set this property to add User Data that installs the CodeDeploy agent on the instances.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/codedeploy/latest/userguide/codedeploy-agent-operations-install.html
        """
        return self._values.get('install_agent')

    @property
    def load_balancer(self) -> typing.Optional["LoadBalancer"]:
        """The load balancer to place in front of this Deployment Group. Can be created from either a classic Elastic Load Balancer, or an Application Load Balancer / Network Load Balancer Target Group.

        default
        :default: - Deployment Group will not have a load balancer defined.
        """
        return self._values.get('load_balancer')

    @property
    def on_premise_instance_tags(self) -> typing.Optional["InstanceTagSet"]:
        """All on-premise instances matching the given set of tags when a deployment occurs will be added to this Deployment Group.

        default
        :default: - No additional on-premise instances will be added to the Deployment Group.
        """
        return self._values.get('on_premise_instance_tags')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The service Role of this Deployment Group.

        default
        :default: - A new Role will be created.
        """
        return self._values.get('role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ServerDeploymentGroupProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["AutoRollbackConfig", "CfnApplication", "CfnApplicationProps", "CfnDeploymentConfig", "CfnDeploymentConfigProps", "CfnDeploymentGroup", "CfnDeploymentGroupProps", "EcsApplication", "EcsApplicationProps", "EcsDeploymentConfig", "EcsDeploymentGroup", "EcsDeploymentGroupAttributes", "IEcsApplication", "IEcsDeploymentConfig", "IEcsDeploymentGroup", "ILambdaApplication", "ILambdaDeploymentConfig", "ILambdaDeploymentGroup", "IServerApplication", "IServerDeploymentConfig", "IServerDeploymentGroup", "InstanceTagSet", "LambdaApplication", "LambdaApplicationProps", "LambdaDeploymentConfig", "LambdaDeploymentConfigImportProps", "LambdaDeploymentGroup", "LambdaDeploymentGroupAttributes", "LambdaDeploymentGroupProps", "LoadBalancer", "LoadBalancerGeneration", "MinimumHealthyHosts", "ServerApplication", "ServerApplicationProps", "ServerDeploymentConfig", "ServerDeploymentConfigProps", "ServerDeploymentGroup", "ServerDeploymentGroupAttributes", "ServerDeploymentGroupProps", "__jsii_assembly__"]

publication.publish()
