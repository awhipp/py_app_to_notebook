import pytest
import os
import shutil

from py2databricks.utilities.dir_utils import create_temporary_directory

@pytest.fixture
def output_dependency_string():
    """Output of the dependency tree."""
    
    return """sample_application.app
----sample_application.utilities.driver
--------sample_application.utilities.environment.variables
------------sample_application.utilities.generators.randoms
"""

@pytest.fixture
def output_dependency_paths():
    """Output of the dependency paths as a list."""

    return [
        f'sample_application{os.sep}app.py',
        f'sample_application{os.sep}utilities{os.sep}driver.py',
        f'sample_application{os.sep}utilities{os.sep}environment{os.sep}variables.py',
        f'sample_application{os.sep}utilities{os.sep}generators{os.sep}randoms.py',
    ]


@pytest.fixture
def output_dependency_paths_ordered():
    """Output of the dependency paths as a list ordered."""

    return [
        f'sample_application{os.sep}utilities{os.sep}generators{os.sep}randoms.py',
        f'sample_application{os.sep}utilities{os.sep}environment{os.sep}variables.py',
        f'sample_application{os.sep}utilities{os.sep}driver.py',
        f'sample_application{os.sep}app.py',
    ]

@pytest.fixture
def output_dependency_tree_keys():
    """Output of the dependency tree as keys."""

    return [
        'sample_application.app', 
        'sample_application.utilities.driver', 
        'sample_application.utilities.environment.variables', 
        'sample_application.utilities.generators.randoms'
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