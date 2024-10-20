from aws_cdk import App
from aws_cdk.assertions import Template

from s3_bi_crr import S3BucketsWithCrrStack, S3BucketsWithCrrStackProps


def test_bucket_stack_synthesizes_properly(snapshot_json):
    app = App(
        context={
            "aws:cdk:bundling-stacks": [],
        },
    )

    # Properties
    properties = S3BucketsWithCrrStackProps(
        bucket_name_prefix="test-prefix",
        region_alpha="eu-west-1",
        region_bravo="eu-central-1",
    )

    # Create test stack
    overall_stack = S3BucketsWithCrrStack(
        app,
        "TestS3CrrStack",
        properties=properties,
    )

    test_stack = overall_stack.alpha_bucket_stack

    # Get Template
    template = Template.from_stack(test_stack)

    assert template.to_json() == snapshot_json()

    # Run cdk-nag
    # TODO: Fix later, not relevant for an example.
    # Aspects.of(test_stack).add(AwsSolutionsChecks(verbose=True))

    # nag_warnings = Annotations.from_stack(test_stack).find_warning("*", Match.string_like_regexp("AwsSolutions-.*"))
    # assert nag_warnings == []

    # nag_errors = Annotations.from_stack(test_stack).find_error("*", Match.string_like_regexp("AwsSolutions-.*"))
    # assert nag_errors == []


def test_crr_stack_synthesizes_properly(snapshot_json):
    app = App(
        context={
            "aws:cdk:bundling-stacks": [],
        },
    )

    # Properties
    properties = S3BucketsWithCrrStackProps(
        bucket_name_prefix="test-prefix",
        region_alpha="eu-west-1",
        region_bravo="eu-central-1",
    )

    # Create test stack
    overall_stack = S3BucketsWithCrrStack(
        app,
        "TestS3CrrStack",
        properties=properties,
    )

    test_stack = overall_stack.alpha_bucket_crr_stack

    # Get Template
    template = Template.from_stack(test_stack)

    assert template.to_json() == snapshot_json()

    # Run cdk-nag
    # TODO: Fix later, not relevant for an example.
    # Aspects.of(test_stack).add(AwsSolutionsChecks(verbose=True))

    # nag_warnings = Annotations.from_stack(test_stack).find_warning("*", Match.string_like_regexp("AwsSolutions-.*"))
    # assert nag_warnings == []

    # nag_errors = Annotations.from_stack(test_stack).find_error("*", Match.string_like_regexp("AwsSolutions-.*"))
    # assert nag_errors == []


def test_overall_stack_synthesizes_properly(snapshot_json):
    app = App(
        context={
            "aws:cdk:bundling-stacks": [],
        },
    )

    # Properties
    properties = S3BucketsWithCrrStackProps(
        bucket_name_prefix="test-prefix",
        region_alpha="eu-west-1",
        region_bravo="eu-central-1",
    )

    # Create test stack
    test_stack = S3BucketsWithCrrStack(
        app,
        "TestS3CrrStack",
        properties=properties,
    )

    # Get Template
    template = Template.from_stack(test_stack)

    assert template.to_json() == snapshot_json()

    # Run cdk-nag
    # TODO: Fix later, not relevant for an example.
    # Aspects.of(test_stack).add(AwsSolutionsChecks(verbose=True))

    # nag_warnings = Annotations.from_stack(test_stack).find_warning("*", Match.string_like_regexp("AwsSolutions-.*"))
    # assert nag_warnings == []

    # nag_errors = Annotations.from_stack(test_stack).find_error("*", Match.string_like_regexp("AwsSolutions-.*"))
    # assert nag_errors == []
