from aws_cdk import Stack
from pydantic import BaseModel

from s3_bi_crr.bucket_stack import S3BucketStack, S3BucketStackProps
from s3_bi_crr.crr_stack import CrrStack, CrrStackProps
from s3_bi_crr.shared import Bucket


class S3BucketsWithCrrStackProps(BaseModel):
    bucket_name_prefix: str
    region_alpha: str
    region_bravo: str


class S3BucketsWithCrrStack(Stack):
    def __init__(self, scope: Stack, id: str, properties: S3BucketsWithCrrStackProps, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.id = id
        self.props = properties

        # Alpha Region Bucket
        alpha_bucket = Bucket(
            name_prefix=self.props.bucket_name_prefix,
            account_number=self.account,
            region=self.props.region_alpha,
        )
        self.alpha_bucket_stack = S3BucketStack(
            self,
            f"{self.id}Alpha",
            S3BucketStackProps(bucket=alpha_bucket),
            env={"region": self.props.region_alpha},
        )

        # Bravo Region Bucket
        bravo_bucket = Bucket(
            name_prefix=self.props.bucket_name_prefix,
            account_number=self.account,
            region=self.props.region_bravo,
        )
        self.bravo_bucket_stack = S3BucketStack(
            self,
            f"{self.id}Bravo",
            S3BucketStackProps(bucket=bravo_bucket),
            env={"region": self.props.region_bravo},
        )

        # CRR Stacks
        self.alpha_bucket_crr_stack = CrrStack(
            self,
            f"{self.id}AlphaToBravo",
            CrrStackProps(source_bucket=alpha_bucket, target_bucket=bravo_bucket),
            env={"region": self.props.region_alpha},
        )
        self.alpha_bucket_crr_stack.node.add_dependency(self.alpha_bucket_stack, self.bravo_bucket_stack)
        self.bravo_bucket_crr_stack = CrrStack(
            self,
            f"{self.id}BravoToAlpha",
            CrrStackProps(source_bucket=bravo_bucket, target_bucket=alpha_bucket),
            env={"region": self.props.region_bravo},
        )
        self.bravo_bucket_crr_stack.node.add_dependency(self.alpha_bucket_stack, self.bravo_bucket_stack)
