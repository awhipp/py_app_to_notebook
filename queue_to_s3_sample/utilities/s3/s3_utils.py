"""
S3 helper functions
"""

# Relative path should be `%run ../boto_helpers.py`
from queue_to_s3_sample.utilities.boto_helpers import get_client

def create_bucket_if_not_exists(bucket_name:str, s3_client=None):
    """
    Creates an S3 bucket if it doesn't already exist
    """
    if not s3_client:
        s3_client = get_client('s3')
    s3_client.create_bucket(Bucket=bucket_name)


def delete_bucket(bucket_name:str, s3_client=None):
    """
    Deletes an S3 bucket and all contents
    """
    if not s3_client:
        s3_client = get_client('s3')

    # delete all objects
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
    
    # delete bucket
    s3_client.delete_bucket(Bucket=bucket_name)

def push_string_to_s3(bucket_name:str, key:str, string:str, s3_client=None):
    """
    Pushes a string to an S3 bucket
    """
    if not s3_client:
        s3_client = get_client('s3')

    create_bucket_if_not_exists(bucket_name)

    s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=string
    )