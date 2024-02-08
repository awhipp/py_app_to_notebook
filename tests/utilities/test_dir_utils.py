"""Test the directory utilities."""
import os
from py2databricks.utilities.dir_utils import module_name_to_path, create_temporary_directory, move_file_to_directory, archive_directory

def test_module_name_to_path():
    """Test the module name to path conversion."""
    # ARRANGE
    module_name = "py2databricks.utilities.dir_utils"

    # ACT
    path = module_name_to_path(module_name)

    # ASSERT
    assert path == "py2databricks/utilities/dir_utils.py".replace('/', os.sep)

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

def test_archive_directory():
    """Test archiving a directory."""
    # ARRANGE
    temporary_directory = create_temporary_directory()

    # Recursively copy tests to the temporary directory
    for root, _, filenames in os.walk("tests"):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            move_file_to_directory(file_path, temporary_directory)
    
    archive_path = temporary_directory + os.sep + "test_archive.zip"

    # ACT
    archive_directory(f"{temporary_directory}{os.sep}tests", archive_path)

    # ASSERT
    # Archive exists
    assert os.path.exists(archive_path)
    # Archive is a file
    assert not os.path.isdir(archive_path)
    # Original directory does not exist
    assert not os.path.exists(temporary_directory + os.sep + "tests")

