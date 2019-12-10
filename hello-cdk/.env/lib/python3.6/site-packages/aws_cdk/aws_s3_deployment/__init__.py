import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_cloudfront
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_s3_assets
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3-deployment", "1.15.0", __name__, "aws-s3-deployment@1.15.0.jsii.tgz")
class BucketDeployment(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.BucketDeployment"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, destination_bucket: aws_cdk.aws_s3.IBucket, sources: typing.List["ISource"], cache_control: typing.Optional[typing.List["CacheControl"]]=None, content_disposition: typing.Optional[str]=None, content_encoding: typing.Optional[str]=None, content_language: typing.Optional[str]=None, content_type: typing.Optional[str]=None, destination_key_prefix: typing.Optional[str]=None, distribution: typing.Optional[aws_cdk.aws_cloudfront.IDistribution]=None, distribution_paths: typing.Optional[typing.List[str]]=None, expires: typing.Optional["Expires"]=None, memory_limit: typing.Optional[jsii.Number]=None, metadata: typing.Optional["UserDefinedObjectMetadata"]=None, retain_on_delete: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, server_side_encryption: typing.Optional["ServerSideEncryption"]=None, server_side_encryption_aws_kms_key_id: typing.Optional[str]=None, server_side_encryption_customer_algorithm: typing.Optional[str]=None, storage_class: typing.Optional["StorageClass"]=None, website_redirect_location: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param destination_bucket: The S3 bucket to sync the contents of the zip file to.
        :param sources: The sources from which to deploy the contents of this bucket.
        :param cache_control: System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
        :param distribution: The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param expires: System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param retain_on_delete: If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Default: - Not set.
        :param storage_class: System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param website_redirect_location: System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        stability
        :stability: experimental
        """
        props = BucketDeploymentProps(destination_bucket=destination_bucket, sources=sources, cache_control=cache_control, content_disposition=content_disposition, content_encoding=content_encoding, content_language=content_language, content_type=content_type, destination_key_prefix=destination_key_prefix, distribution=distribution, distribution_paths=distribution_paths, expires=expires, memory_limit=memory_limit, metadata=metadata, retain_on_delete=retain_on_delete, role=role, server_side_encryption=server_side_encryption, server_side_encryption_aws_kms_key_id=server_side_encryption_aws_kms_key_id, server_side_encryption_customer_algorithm=server_side_encryption_customer_algorithm, storage_class=storage_class, website_redirect_location=website_redirect_location)

        jsii.create(BucketDeployment, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.BucketDeploymentProps", jsii_struct_bases=[], name_mapping={'destination_bucket': 'destinationBucket', 'sources': 'sources', 'cache_control': 'cacheControl', 'content_disposition': 'contentDisposition', 'content_encoding': 'contentEncoding', 'content_language': 'contentLanguage', 'content_type': 'contentType', 'destination_key_prefix': 'destinationKeyPrefix', 'distribution': 'distribution', 'distribution_paths': 'distributionPaths', 'expires': 'expires', 'memory_limit': 'memoryLimit', 'metadata': 'metadata', 'retain_on_delete': 'retainOnDelete', 'role': 'role', 'server_side_encryption': 'serverSideEncryption', 'server_side_encryption_aws_kms_key_id': 'serverSideEncryptionAwsKmsKeyId', 'server_side_encryption_customer_algorithm': 'serverSideEncryptionCustomerAlgorithm', 'storage_class': 'storageClass', 'website_redirect_location': 'websiteRedirectLocation'})
class BucketDeploymentProps():
    def __init__(self, *, destination_bucket: aws_cdk.aws_s3.IBucket, sources: typing.List["ISource"], cache_control: typing.Optional[typing.List["CacheControl"]]=None, content_disposition: typing.Optional[str]=None, content_encoding: typing.Optional[str]=None, content_language: typing.Optional[str]=None, content_type: typing.Optional[str]=None, destination_key_prefix: typing.Optional[str]=None, distribution: typing.Optional[aws_cdk.aws_cloudfront.IDistribution]=None, distribution_paths: typing.Optional[typing.List[str]]=None, expires: typing.Optional["Expires"]=None, memory_limit: typing.Optional[jsii.Number]=None, metadata: typing.Optional["UserDefinedObjectMetadata"]=None, retain_on_delete: typing.Optional[bool]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, server_side_encryption: typing.Optional["ServerSideEncryption"]=None, server_side_encryption_aws_kms_key_id: typing.Optional[str]=None, server_side_encryption_customer_algorithm: typing.Optional[str]=None, storage_class: typing.Optional["StorageClass"]=None, website_redirect_location: typing.Optional[str]=None):
        """
        :param destination_bucket: The S3 bucket to sync the contents of the zip file to.
        :param sources: The sources from which to deploy the contents of this bucket.
        :param cache_control: System-defined cache-control metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_disposition: System-defined cache-disposition metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_encoding: System-defined content-encoding metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_language: System-defined content-language metadata to be set on all objects in the deployment. Default: - Not set.
        :param content_type: System-defined content-type metadata to be set on all objects in the deployment. Default: - Not set.
        :param destination_key_prefix: Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
        :param distribution: The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket. Default: - No invalidation occurs
        :param distribution_paths: The file paths to invalidate in the CloudFront distribution. Default: - All files under the destination bucket key prefix will be invalidated.
        :param expires: System-defined expires metadata to be set on all objects in the deployment. Default: - The objects in the distribution will not expire.
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: 128
        :param metadata: User-defined object metadata to be set on all objects in the deployment. Default: - No user metadata is set
        :param retain_on_delete: If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param server_side_encryption: System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment. Default: - Server side encryption is not used.
        :param server_side_encryption_aws_kms_key_id: System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment. Default: - Not set.
        :param server_side_encryption_customer_algorithm: System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment. Default: - Not set.
        :param storage_class: System-defined x-amz-storage-class metadata to be set on all objects in the deployment. Default: - Default storage-class for the bucket is used.
        :param website_redirect_location: System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment. Default: - No website redirection.

        stability
        :stability: experimental
        """
        self._values = {
            'destination_bucket': destination_bucket,
            'sources': sources,
        }
        if cache_control is not None: self._values["cache_control"] = cache_control
        if content_disposition is not None: self._values["content_disposition"] = content_disposition
        if content_encoding is not None: self._values["content_encoding"] = content_encoding
        if content_language is not None: self._values["content_language"] = content_language
        if content_type is not None: self._values["content_type"] = content_type
        if destination_key_prefix is not None: self._values["destination_key_prefix"] = destination_key_prefix
        if distribution is not None: self._values["distribution"] = distribution
        if distribution_paths is not None: self._values["distribution_paths"] = distribution_paths
        if expires is not None: self._values["expires"] = expires
        if memory_limit is not None: self._values["memory_limit"] = memory_limit
        if metadata is not None: self._values["metadata"] = metadata
        if retain_on_delete is not None: self._values["retain_on_delete"] = retain_on_delete
        if role is not None: self._values["role"] = role
        if server_side_encryption is not None: self._values["server_side_encryption"] = server_side_encryption
        if server_side_encryption_aws_kms_key_id is not None: self._values["server_side_encryption_aws_kms_key_id"] = server_side_encryption_aws_kms_key_id
        if server_side_encryption_customer_algorithm is not None: self._values["server_side_encryption_customer_algorithm"] = server_side_encryption_customer_algorithm
        if storage_class is not None: self._values["storage_class"] = storage_class
        if website_redirect_location is not None: self._values["website_redirect_location"] = website_redirect_location

    @property
    def destination_bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 bucket to sync the contents of the zip file to.

        stability
        :stability: experimental
        """
        return self._values.get('destination_bucket')

    @property
    def sources(self) -> typing.List["ISource"]:
        """The sources from which to deploy the contents of this bucket.

        stability
        :stability: experimental
        """
        return self._values.get('sources')

    @property
    def cache_control(self) -> typing.Optional[typing.List["CacheControl"]]:
        """System-defined cache-control metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('cache_control')

    @property
    def content_disposition(self) -> typing.Optional[str]:
        """System-defined cache-disposition metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_disposition')

    @property
    def content_encoding(self) -> typing.Optional[str]:
        """System-defined content-encoding metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_encoding')

    @property
    def content_language(self) -> typing.Optional[str]:
        """System-defined content-language metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_language')

    @property
    def content_type(self) -> typing.Optional[str]:
        """System-defined content-type metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('content_type')

    @property
    def destination_key_prefix(self) -> typing.Optional[str]:
        """Key prefix in the destination bucket.

        default
        :default: "/" (unzip to root of the destination bucket)

        stability
        :stability: experimental
        """
        return self._values.get('destination_key_prefix')

    @property
    def distribution(self) -> typing.Optional[aws_cdk.aws_cloudfront.IDistribution]:
        """The CloudFront distribution using the destination bucket as an origin. Files in the distribution's edge caches will be invalidated after files are uploaded to the destination bucket.

        default
        :default: - No invalidation occurs

        stability
        :stability: experimental
        """
        return self._values.get('distribution')

    @property
    def distribution_paths(self) -> typing.Optional[typing.List[str]]:
        """The file paths to invalidate in the CloudFront distribution.

        default
        :default: - All files under the destination bucket key prefix will be invalidated.

        stability
        :stability: experimental
        """
        return self._values.get('distribution_paths')

    @property
    def expires(self) -> typing.Optional["Expires"]:
        """System-defined expires metadata to be set on all objects in the deployment.

        default
        :default: - The objects in the distribution will not expire.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('expires')

    @property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        """The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket.

        If you are deploying large files, you will need to increase this number
        accordingly.

        default
        :default: 128

        stability
        :stability: experimental
        """
        return self._values.get('memory_limit')

    @property
    def metadata(self) -> typing.Optional["UserDefinedObjectMetadata"]:
        """User-defined object metadata to be set on all objects in the deployment.

        default
        :default: - No user metadata is set

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#UserMetadata
        stability
        :stability: experimental
        """
        return self._values.get('metadata')

    @property
    def retain_on_delete(self) -> typing.Optional[bool]:
        """If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated.

        NOTICE: if this is set to "false" and destination bucket/prefix is updated,
        all files in the previous destination will first be deleted and then
        uploaded to the new destination location. This could have availablity
        implications on your users.

        default
        :default: true - when resource is deleted/updated, files are retained

        stability
        :stability: experimental
        """
        return self._values.get('retain_on_delete')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """Execution role associated with this function.

        default
        :default: - A role is automatically created

        stability
        :stability: experimental
        """
        return self._values.get('role')

    @property
    def server_side_encryption(self) -> typing.Optional["ServerSideEncryption"]:
        """System-defined x-amz-server-side-encryption metadata to be set on all objects in the deployment.

        default
        :default: - Server side encryption is not used.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('server_side_encryption')

    @property
    def server_side_encryption_aws_kms_key_id(self) -> typing.Optional[str]:
        """System-defined x-amz-server-side-encryption-aws-kms-key-id metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('server_side_encryption_aws_kms_key_id')

    @property
    def server_side_encryption_customer_algorithm(self) -> typing.Optional[str]:
        """System-defined x-amz-server-side-encryption-customer-algorithm metadata to be set on all objects in the deployment.

        default
        :default: - Not set.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('server_side_encryption_customer_algorithm')

    @property
    def storage_class(self) -> typing.Optional["StorageClass"]:
        """System-defined x-amz-storage-class metadata to be set on all objects in the deployment.

        default
        :default: - Default storage-class for the bucket is used.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('storage_class')

    @property
    def website_redirect_location(self) -> typing.Optional[str]:
        """System-defined x-amz-website-redirect-location metadata to be set on all objects in the deployment.

        default
        :default: - No website redirection.

        see
        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
        stability
        :stability: experimental
        """
        return self._values.get('website_redirect_location')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'BucketDeploymentProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CacheControl(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.CacheControl"):
    """Used for HTTP cache-control header, which influences downstream caches.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="fromString")
    @classmethod
    def from_string(cls, s: str) -> "CacheControl":
        """
        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @jsii.member(jsii_name="maxAge")
    @classmethod
    def max_age(cls, t: aws_cdk.core.Duration) -> "CacheControl":
        """
        :param t: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "maxAge", [t])

    @jsii.member(jsii_name="mustRevalidate")
    @classmethod
    def must_revalidate(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "mustRevalidate", [])

    @jsii.member(jsii_name="noCache")
    @classmethod
    def no_cache(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noCache", [])

    @jsii.member(jsii_name="noTransform")
    @classmethod
    def no_transform(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "noTransform", [])

    @jsii.member(jsii_name="proxyRevalidate")
    @classmethod
    def proxy_revalidate(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "proxyRevalidate", [])

    @jsii.member(jsii_name="setPrivate")
    @classmethod
    def set_private(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPrivate", [])

    @jsii.member(jsii_name="setPublic")
    @classmethod
    def set_public(cls) -> "CacheControl":
        """
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "setPublic", [])

    @jsii.member(jsii_name="sMaxAge")
    @classmethod
    def s_max_age(cls, t: aws_cdk.core.Duration) -> "CacheControl":
        """
        :param t: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "sMaxAge", [t])

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


class Expires(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.Expires"):
    """Used for HTTP expires header, which influences downstream caches.

    Does NOT influence deletion of the object.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="after")
    @classmethod
    def after(cls, t: aws_cdk.core.Duration) -> "Expires":
        """Expire once the specified duration has passed since deployment time.

        :param t: the duration to wait before expiring.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "after", [t])

    @jsii.member(jsii_name="atDate")
    @classmethod
    def at_date(cls, d: datetime.datetime) -> "Expires":
        """Expire at the specified date.

        :param d: date to expire at.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "atDate", [d])

    @jsii.member(jsii_name="atTimestamp")
    @classmethod
    def at_timestamp(cls, t: jsii.Number) -> "Expires":
        """Expire at the specified timestamp.

        :param t: timestamp in unix milliseconds.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "atTimestamp", [t])

    @jsii.member(jsii_name="fromString")
    @classmethod
    def from_string(cls, s: str) -> "Expires":
        """
        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromString", [s])

    @property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.interface(jsii_type="@aws-cdk/aws-s3-deployment.ISource")
class ISource(jsii.compat.Protocol):
    """Represents a source for bucket deployments.

    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @jsii.member(jsii_name="bind")
    def bind(self, context: aws_cdk.core.Construct) -> "SourceConfig":
        """Binds the source to a bucket deployment.

        :param context: The construct tree context.

        stability
        :stability: experimental
        """
        ...


class _ISourceProxy():
    """Represents a source for bucket deployments.

    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-s3-deployment.ISource"
    @jsii.member(jsii_name="bind")
    def bind(self, context: aws_cdk.core.Construct) -> "SourceConfig":
        """Binds the source to a bucket deployment.

        :param context: The construct tree context.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [context])


@jsii.enum(jsii_type="@aws-cdk/aws-s3-deployment.ServerSideEncryption")
class ServerSideEncryption(enum.Enum):
    """Indicates whether server-side encryption is enabled for the object, and whether that encryption is from the AWS Key Management Service (AWS KMS) or from Amazon S3 managed encryption (SSE-S3).

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    AES_256 = "AES_256"
    """
    stability
    :stability: experimental
    """
    AWS_KMS = "AWS_KMS"
    """
    stability
    :stability: experimental
    """

class Source(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.Source"):
    """Specifies bucket deployment source.

    Usage::

        Source.bucket(bucket, key)
        Source.asset('/local/path/to/directory')
        Source.asset('/local/path/to/a/file.zip')

    stability
    :stability: experimental
    """
    @jsii.member(jsii_name="asset")
    @classmethod
    def asset(cls, path: str) -> "ISource":
        """Uses a local asset as the deployment source.

        :param path: The path to a local .zip file or a directory.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asset", [path])

    @jsii.member(jsii_name="bucket")
    @classmethod
    def bucket(cls, bucket: aws_cdk.aws_s3.IBucket, zip_object_key: str) -> "ISource":
        """Uses a .zip file stored in an S3 bucket as the source for the destination bucket contents.

        :param bucket: The S3 Bucket.
        :param zip_object_key: The S3 object key of the zip file with contents.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "bucket", [bucket, zip_object_key])


@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.SourceConfig", jsii_struct_bases=[], name_mapping={'bucket': 'bucket', 'zip_object_key': 'zipObjectKey'})
class SourceConfig():
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, zip_object_key: str):
        """
        :param bucket: The source bucket to deploy from.
        :param zip_object_key: An S3 object key in the source bucket that points to a zip file.

        stability
        :stability: experimental
        """
        self._values = {
            'bucket': bucket,
            'zip_object_key': zip_object_key,
        }

    @property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The source bucket to deploy from.

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @property
    def zip_object_key(self) -> str:
        """An S3 object key in the source bucket that points to a zip file.

        stability
        :stability: experimental
        """
        return self._values.get('zip_object_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'SourceConfig(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-s3-deployment.StorageClass")
class StorageClass(enum.Enum):
    """Storage class used for storing the object.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html#SysMetadata
    stability
    :stability: experimental
    """
    STANDARD = "STANDARD"
    """
    stability
    :stability: experimental
    """
    REDUCED_REDUNDANCY = "REDUCED_REDUNDANCY"
    """
    stability
    :stability: experimental
    """
    STANDARD_IA = "STANDARD_IA"
    """
    stability
    :stability: experimental
    """
    ONEZONE_IA = "ONEZONE_IA"
    """
    stability
    :stability: experimental
    """
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    """
    stability
    :stability: experimental
    """
    GLACIER = "GLACIER"
    """
    stability
    :stability: experimental
    """
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    """
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.UserDefinedObjectMetadata", jsii_struct_bases=[], name_mapping={})
class UserDefinedObjectMetadata():
    def __init__(self):
        """
        stability
        :stability: experimental
        """
        self._values = {
        }

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'UserDefinedObjectMetadata(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["BucketDeployment", "BucketDeploymentProps", "CacheControl", "Expires", "ISource", "ServerSideEncryption", "Source", "SourceConfig", "StorageClass", "UserDefinedObjectMetadata", "__jsii_assembly__"]

publication.publish()
