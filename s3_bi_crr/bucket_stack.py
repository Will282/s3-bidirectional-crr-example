from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from pydantic import BaseModel

from s3_bi_crr.shared import Bucket


class S3BucketStackProps(BaseModel):
    bucket: Bucket


class S3BucketStack(Stack):
    def __init__(self, scope: Stack, id: str, properties: S3BucketStackProps, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.id = id
        self.props = properties

        self.bucket = s3.CfnBucket(
            self,
            f"{self.id}Bucket",
            bucket_name=self.props.bucket.name,
            versioning_configuration=s3.CfnBucket.VersioningConfigurationProperty(status="Enabled"),
        )
