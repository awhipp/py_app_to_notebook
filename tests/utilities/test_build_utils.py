"""Test the build utilities."""

import os
from py_app_to_notebook.utilities.build_utils import build_temporary_directory

def test_build_temporary_directory(output_dependency_tree_list):
    """Test building a temporary directory."""

    # ACT
    temporary_directory, files_created = build_temporary_directory(f'queue_to_s3_sample{os.sep}app.py')


    # ASSERT

    assert files_created == 4
    
    # Recursively get all files in the directory
    files = []
    for root, _, filenames in os.walk(temporary_directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # Ensure the files are as expected
    for created_file in files:
        assert created_file.replace(f"{temporary_directory}{os.sep}", "") in output_dependency_tree_list
        
    # Recursively delete any empty folders and files
    for root, dirs, files in os.walk(temporary_directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


    
