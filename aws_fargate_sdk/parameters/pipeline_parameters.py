from aws_cdk.aws_s3 import Bucket


class PipelineParams:
    """
    Parameters class which specifies various parameters for ci/cd pipeline.
    """
    def __init__(self, artifact_builds_bucket: Bucket):
        """
        Constructor.
        :param artifact_builds_bucket: An artifacts bucket which will be used by a ci/cd pipeline to write
        and read build/source artifacts.
        """
        self.artifact_builds_bucket = artifact_builds_bucket