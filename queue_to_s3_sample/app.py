"""
Pulls a message from an SQS queue and pushes it to an S3 bucket
"""
from queue_to_s3_sample.aws_helpers.sqs import pull_message_from_queue
from queue_to_s3_sample.aws_helpers.s3 import push_string_to_s3

from queue_to_s3_sample.aws_helpers.boto_helpers import get_client

def main(s3_client=None, sqs_client=None):
    """
    Pulls a message from an SQS queue and pushes it to an S3 bucket
    """

    RESOURCE_NAME = 'test'

    if not s3_client:
        s3_client = get_client('s3')
    if not sqs_client:
        sqs_client = get_client('sqs')

    message = pull_message_from_queue(queue_name=RESOURCE_NAME, sqs_client=sqs_client)
    if message:
        push_string_to_s3(bucket_name=RESOURCE_NAME, key='message.txt', string=message, s3_client=s3_client)

if __name__ == '__main__':
    main()