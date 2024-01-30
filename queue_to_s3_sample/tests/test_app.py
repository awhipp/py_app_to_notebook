"""
Test the core application
"""
from queue_to_s3_sample.app import main

from queue_to_s3_sample.aws_helpers.sqs import push_message_to_queue

from queue_to_s3_sample.aws_helpers.boto_helpers import get_client

def test_end_to_end():
    """
    Test the core application
    """

    # ARRANGE
    s3_client = get_client('s3')
    sqs_client = get_client('sqs')

    push_message_to_queue(
        queue_name='test',
        message='Hello, world!',
        sqs_client=sqs_client
    )

    # ACT
    main(s3_client=s3_client, sqs_client=sqs_client)

    # ASSERT
    response = s3_client.get_object(
        Bucket='test',
        Key='message.txt'
    )

    assert response['Body'].read().decode('utf-8') == 'Hello, world!'