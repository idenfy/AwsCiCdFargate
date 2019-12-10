import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codestar", "1.14.0", __name__, "aws-codestar@1.14.0.jsii.tgz")
class CfnGitHubRepository(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepository"):
    """A CloudFormation ``AWS::CodeStar::GitHubRepository``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeStar::GitHubRepository
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, repository_access_token: str, repository_name: str, repository_owner: str, code: typing.Optional[typing.Union[typing.Optional["CodeProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, enable_issues: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, is_private: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, repository_description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CodeStar::GitHubRepository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param repository_access_token: ``AWS::CodeStar::GitHubRepository.RepositoryAccessToken``.
        :param repository_name: ``AWS::CodeStar::GitHubRepository.RepositoryName``.
        :param repository_owner: ``AWS::CodeStar::GitHubRepository.RepositoryOwner``.
        :param code: ``AWS::CodeStar::GitHubRepository.Code``.
        :param enable_issues: ``AWS::CodeStar::GitHubRepository.EnableIssues``.
        :param is_private: ``AWS::CodeStar::GitHubRepository.IsPrivate``.
        :param repository_description: ``AWS::CodeStar::GitHubRepository.RepositoryDescription``.
        """
        props = CfnGitHubRepositoryProps(repository_access_token=repository_access_token, repository_name=repository_name, repository_owner=repository_owner, code=code, enable_issues=enable_issues, is_private=is_private, repository_description=repository_description)

        jsii.create(CfnGitHubRepository, self, [scope, id, props])

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
    @jsii.member(jsii_name="repositoryAccessToken")
    def repository_access_token(self) -> str:
        """``AWS::CodeStar::GitHubRepository.RepositoryAccessToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryaccesstoken
        """
        return jsii.get(self, "repositoryAccessToken")

    @repository_access_token.setter
    def repository_access_token(self, value: str):
        return jsii.set(self, "repositoryAccessToken", value)

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """``AWS::CodeStar::GitHubRepository.RepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryname
        """
        return jsii.get(self, "repositoryName")

    @repository_name.setter
    def repository_name(self, value: str):
        return jsii.set(self, "repositoryName", value)

    @property
    @jsii.member(jsii_name="repositoryOwner")
    def repository_owner(self) -> str:
        """``AWS::CodeStar::GitHubRepository.RepositoryOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryowner
        """
        return jsii.get(self, "repositoryOwner")

    @repository_owner.setter
    def repository_owner(self, value: str):
        return jsii.set(self, "repositoryOwner", value)

    @property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Optional[typing.Union[typing.Optional["CodeProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStar::GitHubRepository.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        """
        return jsii.get(self, "code")

    @code.setter
    def code(self, value: typing.Optional[typing.Union[typing.Optional["CodeProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "code", value)

    @property
    @jsii.member(jsii_name="enableIssues")
    def enable_issues(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStar::GitHubRepository.EnableIssues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        """
        return jsii.get(self, "enableIssues")

    @enable_issues.setter
    def enable_issues(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "enableIssues", value)

    @property
    @jsii.member(jsii_name="isPrivate")
    def is_private(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStar::GitHubRepository.IsPrivate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        """
        return jsii.get(self, "isPrivate")

    @is_private.setter
    def is_private(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "isPrivate", value)

    @property
    @jsii.member(jsii_name="repositoryDescription")
    def repository_description(self) -> typing.Optional[str]:
        """``AWS::CodeStar::GitHubRepository.RepositoryDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositorydescription
        """
        return jsii.get(self, "repositoryDescription")

    @repository_description.setter
    def repository_description(self, value: typing.Optional[str]):
        return jsii.set(self, "repositoryDescription", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepository.CodeProperty", jsii_struct_bases=[], name_mapping={'s3': 's3'})
    class CodeProperty():
        def __init__(self, *, s3: typing.Union[aws_cdk.core.IResolvable, "CfnGitHubRepository.S3Property"]):
            """
            :param s3: ``CfnGitHubRepository.CodeProperty.S3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html
            """
            self._values = {
                's3': s3,
            }

        @property
        def s3(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnGitHubRepository.S3Property"]:
            """``CfnGitHubRepository.CodeProperty.S3``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-code.html#cfn-codestar-githubrepository-code-s3
            """
            return self._values.get('s3')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CodeProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepository.S3Property", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'key': 'key', 'object_version': 'objectVersion'})
    class S3Property():
        def __init__(self, *, bucket: str, key: str, object_version: typing.Optional[str]=None):
            """
            :param bucket: ``CfnGitHubRepository.S3Property.Bucket``.
            :param key: ``CfnGitHubRepository.S3Property.Key``.
            :param object_version: ``CfnGitHubRepository.S3Property.ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html
            """
            self._values = {
                'bucket': bucket,
                'key': key,
            }
            if object_version is not None: self._values["object_version"] = object_version

        @property
        def bucket(self) -> str:
            """``CfnGitHubRepository.S3Property.Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-bucket
            """
            return self._values.get('bucket')

        @property
        def key(self) -> str:
            """``CfnGitHubRepository.S3Property.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-key
            """
            return self._values.get('key')

        @property
        def object_version(self) -> typing.Optional[str]:
            """``CfnGitHubRepository.S3Property.ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codestar-githubrepository-s3.html#cfn-codestar-githubrepository-s3-objectversion
            """
            return self._values.get('object_version')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3Property(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-codestar.CfnGitHubRepositoryProps", jsii_struct_bases=[], name_mapping={'repository_access_token': 'repositoryAccessToken', 'repository_name': 'repositoryName', 'repository_owner': 'repositoryOwner', 'code': 'code', 'enable_issues': 'enableIssues', 'is_private': 'isPrivate', 'repository_description': 'repositoryDescription'})
class CfnGitHubRepositoryProps():
    def __init__(self, *, repository_access_token: str, repository_name: str, repository_owner: str, code: typing.Optional[typing.Union[typing.Optional["CfnGitHubRepository.CodeProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, enable_issues: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, is_private: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, repository_description: typing.Optional[str]=None):
        """Properties for defining a ``AWS::CodeStar::GitHubRepository``.

        :param repository_access_token: ``AWS::CodeStar::GitHubRepository.RepositoryAccessToken``.
        :param repository_name: ``AWS::CodeStar::GitHubRepository.RepositoryName``.
        :param repository_owner: ``AWS::CodeStar::GitHubRepository.RepositoryOwner``.
        :param code: ``AWS::CodeStar::GitHubRepository.Code``.
        :param enable_issues: ``AWS::CodeStar::GitHubRepository.EnableIssues``.
        :param is_private: ``AWS::CodeStar::GitHubRepository.IsPrivate``.
        :param repository_description: ``AWS::CodeStar::GitHubRepository.RepositoryDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html
        """
        self._values = {
            'repository_access_token': repository_access_token,
            'repository_name': repository_name,
            'repository_owner': repository_owner,
        }
        if code is not None: self._values["code"] = code
        if enable_issues is not None: self._values["enable_issues"] = enable_issues
        if is_private is not None: self._values["is_private"] = is_private
        if repository_description is not None: self._values["repository_description"] = repository_description

    @property
    def repository_access_token(self) -> str:
        """``AWS::CodeStar::GitHubRepository.RepositoryAccessToken``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryaccesstoken
        """
        return self._values.get('repository_access_token')

    @property
    def repository_name(self) -> str:
        """``AWS::CodeStar::GitHubRepository.RepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryname
        """
        return self._values.get('repository_name')

    @property
    def repository_owner(self) -> str:
        """``AWS::CodeStar::GitHubRepository.RepositoryOwner``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositoryowner
        """
        return self._values.get('repository_owner')

    @property
    def code(self) -> typing.Optional[typing.Union[typing.Optional["CfnGitHubRepository.CodeProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStar::GitHubRepository.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-code
        """
        return self._values.get('code')

    @property
    def enable_issues(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStar::GitHubRepository.EnableIssues``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-enableissues
        """
        return self._values.get('enable_issues')

    @property
    def is_private(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::CodeStar::GitHubRepository.IsPrivate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-isprivate
        """
        return self._values.get('is_private')

    @property
    def repository_description(self) -> typing.Optional[str]:
        """``AWS::CodeStar::GitHubRepository.RepositoryDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codestar-githubrepository.html#cfn-codestar-githubrepository-repositorydescription
        """
        return self._values.get('repository_description')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnGitHubRepositoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CfnGitHubRepository", "CfnGitHubRepositoryProps", "__jsii_assembly__"]

publication.publish()
