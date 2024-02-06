import pytest
import os

@pytest.fixture
def output_dependency_tree():
    """Output of the dependency tree."""
    
    expected_tree = """app (queue_to_s3_sample/app.py)
----app.sqs_utils (queue_to_s3_sample/utilities/sqs/sqs_utils.py)
--------app.sqs_utils.boto_helpers (queue_to_s3_sample/utilities/boto_helpers.py)
----app.s3_utils (queue_to_s3_sample/utilities/s3/s3_utils.py)
--------app.s3_utils.boto_helpers (queue_to_s3_sample/utilities/boto_helpers.py)
----app.boto_helpers (queue_to_s3_sample/utilities/boto_helpers.py)\n"""
    expected_tree = expected_tree.replace('/', os.sep)

    return expected_tree


@pytest.fixture
def output_dependency_tree_list():
    """Output of the dependency tree as a list."""
    expected_list = [
        'queue_to_s3_sample/app.py',
        'queue_to_s3_sample/utilities/sqs/sqs_utils.py',
        'queue_to_s3_sample/utilities/boto_helpers.py',
        'queue_to_s3_sample/utilities/s3/s3_utils.py',
    ]

    for idx, item in enumerate(expected_list):
        expected_list[idx] = item.replace('/', os.sep)

    return expected_list