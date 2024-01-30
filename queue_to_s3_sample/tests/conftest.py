"""
Configuration file for pytest
"""
import os
import pytest

from queue_to_s3_sample.aws_helpers.s3 import create_bucket_if_not_exists, delete_bucket
from queue_to_s3_sample.aws_helpers.sqs import create_queue_if_not_exists, delete_queue

from queue_to_s3_sample.aws_helpers.boto_helpers import get_client

os.environ.setdefault('IS_TESTING', 'true')

RESOURCE_NAME: str = 'test'

s3_client = get_client('s3')
sqs_client = get_client('sqs')

@pytest.fixture(autouse=True)
def create_s3_bucket():
    """
    Creates an S3 bucket for testing
    """

    create_bucket_if_not_exists(bucket_name=RESOURCE_NAME, s3_client=s3_client)

    yield RESOURCE_NAME

    delete_bucket(bucket_name=RESOURCE_NAME, s3_client=s3_client)


@pytest.fixture(autouse=True)
def create_sqs_queue():
    """
    Creates an SQS queue for testing
    """

    create_queue_if_not_exists(queue_name=RESOURCE_NAME, sqs_client=sqs_client)

    yield RESOURCE_NAME

    delete_queue(queue_name=RESOURCE_NAME, sqs_client=sqs_client)
