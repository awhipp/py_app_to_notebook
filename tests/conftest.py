import pytest
import os
import shutil

from py2databricks.utilities.dir_utils import create_temporary_directory

@pytest.fixture
def output_dependency_string():
    """Output of the dependency tree."""
    
    return """queue_to_s3_sample.app
----queue_to_s3_sample.utilities.sqs.sqs_utils
--------queue_to_s3_sample.utilities.boto_helpers
----queue_to_s3_sample.utilities.s3.s3_utils
--------queue_to_s3_sample.utilities.boto_helpers
----queue_to_s3_sample.utilities.boto_helpers
"""

@pytest.fixture
def output_dependency_paths():
    """Output of the dependency paths as a list."""

    return [
        f'queue_to_s3_sample{os.sep}app.py',
        f'queue_to_s3_sample{os.sep}utilities{os.sep}sqs{os.sep}sqs_utils.py',
        f'queue_to_s3_sample{os.sep}utilities{os.sep}boto_helpers.py',
        f'queue_to_s3_sample{os.sep}utilities{os.sep}s3{os.sep}s3_utils.py'
    ]


@pytest.fixture
def output_dependency_paths_ordered():
    """Output of the dependency paths as a list ordered."""

    return [
        f'queue_to_s3_sample{os.sep}utilities{os.sep}boto_helpers.py',
        f'queue_to_s3_sample{os.sep}utilities{os.sep}sqs{os.sep}sqs_utils.py',
        f'queue_to_s3_sample{os.sep}utilities{os.sep}s3{os.sep}s3_utils.py',
        f'queue_to_s3_sample{os.sep}app.py',
    ]

@pytest.fixture
def output_dependency_tree_keys():
    """Output of the dependency tree as keys."""

    return [
        'queue_to_s3_sample.app', 
        'queue_to_s3_sample.utilities.sqs.sqs_utils', 
        'queue_to_s3_sample.utilities.boto_helpers', 
        'queue_to_s3_sample.utilities.s3.s3_utils'
    ]


@pytest.fixture(autouse=True)
def generate_temporary_directory(mocker):
    """Generate a temporary directory for testing."""
    temporary_directory = create_temporary_directory()

    mocker.patch('tempfile.mkdtemp', return_value=temporary_directory)
    
    yield temporary_directory

    # Cleanup
    if os.path.exists(temporary_directory):
        # Force delete
        shutil.rmtree(temporary_directory)