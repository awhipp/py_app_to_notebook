"""Test the directory utilities."""
import os
from py_app_to_notebook.utilities.dir_utils import module_name_to_path, create_temporary_directory, move_file_to_directory

def test_module_name_to_path():
    """Test the module name to path conversion."""
    # ARRANGE
    module_name = "py_app_to_notebook.utilities.dir_utils"

    # ACT
    path = module_name_to_path(module_name)

    # ASSERT
    assert path == "py_app_to_notebook/utilities/dir_utils.py".replace('/', os.sep)

def test_create_temporary_directory():
    """Test the creation of a temporary directory."""
    # ACT
    path = create_temporary_directory()

    # ASSERT
    assert os.path.exists(path)
    os.rmdir(path)

def test_move_file_to_directory():
    """Test moving a file to a directory."""
    # ARRANGE
    file_path = f"tests{os.sep}utilities{os.sep}test_dir_utils.py"
    directory_root = create_temporary_directory()

    # ACT
    new_path = move_file_to_directory(file_path, directory_root)

    # ASSERT

    # Count files in directory_root
    files = []
    for root, _, filenames in os.walk(directory_root):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    assert len(files) == 1
    assert os.path.exists(new_path)
    os.remove(new_path)
    
    # Recursively delete any empty folders (not files)
    for root, dirs, _ in os.walk(directory_root, topdown=False):
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    # Ensure the directory is empty
    assert len(os.listdir(directory_root)) == 0

    # Remove the directory
    os.rmdir(directory_root)
