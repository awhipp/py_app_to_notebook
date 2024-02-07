"""
SQS helper functions
"""

# Relative path should be `%run ../boto_helpers.py`
from queue_to_s3_sample.utilities.boto_helpers import get_client

def create_queue_if_not_exists(queue_name:str, sqs_client=None):
    """
    Creates an SQS queue if it doesn't already exist
    """
    if not sqs_client:
        sqs_client = get_client('sqs')

    try:
        sqs_client.create_queue(QueueName=queue_name)
    except Exception as e:
        if 'QueueAlreadyExists' not in str(e):
            raise e

def delete_queue(queue_name:str, sqs_client=None):
    """
    Deletes an SQS queue
    """
    if not sqs_client:
        sqs_client = get_client('sqs')

    queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    sqs_client.delete_queue(QueueUrl=queue_url)

def pull_message_from_queue(queue_name:str, sqs_client=None):
    """
    Pulls a message from an SQS queue
    """
    if not sqs_client:
        sqs_client = get_client('sqs')

    queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return message['Body']
    else:
        return None
    
def push_message_to_queue(queue_name:str, message:str, sqs_client=None):
    """
    Pushes a message to an SQS queue
    """
    if not sqs_client:
        sqs_client = get_client('sqs')

    queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
    sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message
    )
