import aws_cdk as cdk

from s3_bi_crr import S3BucketsWithCrrStack, S3BucketsWithCrrStackProps

properties = S3BucketsWithCrrStackProps(
    bucket_name_prefix="test-replication",
    region_alpha="eu-west-1",
    region_bravo="eu-central-1",
)

app = cdk.App()
s3_crr_stack = S3BucketsWithCrrStack(
    app,
    "S3BiCrrStack",
    properties=properties,
)

app.synth()
