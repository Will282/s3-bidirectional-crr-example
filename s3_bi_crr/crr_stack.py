from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import custom_resources as cr
from pydantic import BaseModel

from s3_bi_crr.shared import Bucket


class CrrStackProps(BaseModel):
    source_bucket: Bucket
    target_bucket: Bucket


class CrrStack(Stack):
    def __init__(self, scope: Stack, id: str, properties: CrrStackProps, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.id = id
        self.props = properties

        self.replication_role = self._create_replication_role()
        self.replication_config = self._apply_crr_rule()

    def _create_replication_role(self) -> iam.Role:
        # Docs: https://docs.aws.amazon.com/AmazonS3/latest/userguide/setting-repl-config-perm-overview.html
        replication_role = iam.Role(
            self,
            f"{self.id}ReplicationRole",
            assumed_by=iam.ServicePrincipal("s3.amazonaws.com"),
        )
        # Grant necessary permissions for replication
        replication_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:GetReplicationConfiguration", "s3:ListBucket"],
                resources=[self.props.source_bucket.arn],
            )
        )

        replication_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:GetObjectVersionForReplication", "s3:GetObjectVersionAcl", "s3:GetObjectVersionTagging"],
                resources=[f"{self.props.source_bucket.arn}/*"],
            )
        )

        replication_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:ReplicateObject", "s3:ReplicateDelete", "s3:ReplicateTags"],
                resources=[f"{self.props.target_bucket.arn}/*"],
            )
        )

        return replication_role

    def _apply_crr_rule(self) -> cr.AwsCustomResource:
        # Replication config dictionary
        # Main Docs: https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-add-config.html
        # Note as we're using CDK/CFN, it's JSON not XML, see CLI or SDK examples here:
        # https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-walkthrough1.html
        replication_config_dict = {
            "Role": self.replication_role.role_arn,
            "Rules": [
                {
                    "ID": f"{self.props.source_bucket.region}-to-{self.props.target_bucket.region}",
                    "Status": "Enabled",
                    "Priority": 1,
                    "Filter": {"Prefix": ""},  # Replicate all objects
                    "DeleteMarkerReplication": {"Status": "Enabled"},
                    "SourceSelectionCriteria": {
                        # TODO: Support KMS key
                        # "SseKmsEncryptedObjects": {"Status": "Enabled"},
                        "ReplicaModifications": {"Status": "Enabled"},
                    },
                    "Destination": {
                        "Bucket": self.props.target_bucket.arn,
                        "StorageClass": "STANDARD",
                    },
                }
            ],
        }

        replication_config_resource = cr.AwsCustomResource(
            self,
            "PutS3Replication",
            on_create={
                "service": "S3",
                "action": "PutBucketReplication",
                "parameters": {
                    "Bucket": self.props.source_bucket.name,
                    "ReplicationConfiguration": replication_config_dict,
                },
                "physical_resource_id": cr.PhysicalResourceId.of(f"s3-replication-{self.props.source_bucket.name}"),
            },
            on_update={
                "service": "S3",
                "action": "PutBucketReplication",
                "parameters": {
                    "Bucket": self.props.source_bucket.name,
                    "ReplicationConfiguration": replication_config_dict,
                },
                "physical_resource_id": cr.PhysicalResourceId.of(f"s3-replication-{self.props.source_bucket.name}"),
            },
            on_delete={
                "service": "S3",
                "action": "DeleteBucketReplication",
                "parameters": {"Bucket": self.props.source_bucket.name},
            },
            policy=cr.AwsCustomResourcePolicy.from_statements(
                [
                    iam.PolicyStatement(
                        actions=[
                            "s3:GetReplicationConfiguration",
                            "s3:PutReplicationConfiguration",
                        ],
                        resources=[f"arn:aws:s3:::{self.props.source_bucket.name}"],
                    ),
                    iam.PolicyStatement(
                        actions=["iam:PassRole"],
                        resources=[self.replication_role.role_arn],
                    ),
                ]
            ),
        )

        return replication_config_resource
