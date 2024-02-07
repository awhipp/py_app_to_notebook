"""
Pulls a message from an SQS queue and pushes it to an S3 bucket
"""

# Relative path should be `%run utilities/sqs/sqs_utils.py`
# Relative path should be `%run utilities/s3/s3_utils.py`
# Relative path should be `%run utilities/boto_helpers.py`
from queue_to_s3_sample.utilities.sqs.sqs_utils import pull_message_from_queue
from queue_to_s3_sample.utilities.s3.s3_utils import push_string_to_s3

from queue_to_s3_sample.utilities.boto_helpers import get_client

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