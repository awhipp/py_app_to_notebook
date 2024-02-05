import pytest
import os

@pytest.fixture
def output_dependency_tree():
    """Output of the dependency tree."""
    
    expected_tree = """app (queue_to_s3_sample/app.py)
----app.sqs (queue_to_s3_sample/aws_helpers/sqs.py)
--------app.sqs.boto_helpers (queue_to_s3_sample/aws_helpers/boto_helpers.py)
----app.s3 (queue_to_s3_sample/aws_helpers/s3.py)
--------app.s3.boto_helpers (queue_to_s3_sample/aws_helpers/boto_helpers.py)
----app.boto_helpers (queue_to_s3_sample/aws_helpers/boto_helpers.py)
"""
    expected_tree = expected_tree.replace('/', os.sep)

    return expected_tree


@pytest.fixture
def output_dependency_tree_list():
    """Output of the dependency tree as a list."""
    expected_list = [
        'queue_to_s3_sample/app.py',
        'queue_to_s3_sample/aws_helpers/sqs.py',
        'queue_to_s3_sample/aws_helpers/boto_helpers.py',
        'queue_to_s3_sample/aws_helpers/s3.py',
    ]

    for idx, item in enumerate(expected_list):
        expected_list[idx] = item.replace('/', os.sep)

    return expected_list