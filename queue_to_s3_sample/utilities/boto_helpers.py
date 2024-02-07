"""
Generate boto3 client and resources for various services.
"""

# No changes needed to imports
import os
import boto3
import logging

# Define localstack endpoint URLs
localstack_endpoint_urls = {
    's3': 'http://localhost:4566',
    'sqs': 'http://localhost:4566',
}

logger = logging.getLogger(__name__)

session = boto3.session.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=os.environ.get("AWS_REGION", "us-east-1"),
)

def get_client(service_name:str, endpoint_url:str=None):
    """
    Returns a boto3 client for a given service
    """
    if os.environ.get('IS_TESTING', "false").lower() == "true":
        logger.info(f"Using localstack endpoint for {service_name}")
        return session.client(service_name, endpoint_url=localstack_endpoint_urls[service_name])
    
    if endpoint_url:
        logger.info(f"Using endpoint {endpoint_url} for {service_name}")
        return session.client(service_name, endpoint_url=endpoint_url)
    
    logger.info(f"Using default endpoint for {service_name}")
    return session.client(service_name)

def get_resource(service_name:str, endpoint_url:str=None):
    """
    Returns a boto3 resource for a given service
    """
    if os.environ.get('IS_TESTING', "false").lower() == "true":
        logger.info(f"Using localstack endpoint for {service_name}")
        return session.resource(service_name, endpoint_url=localstack_endpoint_urls[service_name])
    
    if endpoint_url:
        logger.info(f"Using endpoint {endpoint_url} for {service_name}")
        return session.resource(service_name, endpoint_url=endpoint_url)
    
    logger.info(f"Using default endpoint for {service_name}")
    return session.resource(service_name)
