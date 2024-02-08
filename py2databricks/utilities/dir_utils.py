"""
Directory utilities, specifically used to determine the dependencies of a Python app.
"""
import os
import shutil
import tempfile

def module_name_to_path(module_name: str) -> str:
    """
    Convert a module name to a path.

    Args:
    - module_name (str): The name of the module.

    Returns:
    - str: The path to the module.
    """
    return module_name.replace('.', os.sep) + '.py'

def path_to_module_name(path: str) -> str:
    """
    Convert a path to a module name.

    Args:
    - path (str): The path to the module.

    Returns:
    - str: The name of the module.
    """
    return path.replace(os.sep, '.').replace('.py', '')

def create_temporary_directory() -> str:
    """
    Create a temporary directory.

    Returns:
    - str: The path to the temporary directory.
    """
    return tempfile.mkdtemp()

def move_file_to_directory(file_path: str, directory_root: str) -> str:
    """
    Copy a file to a directory root, keeping the file heirarchy.

    Args:
    - file_path (str): The path to the file.
    - directory_root (str): The root of the directory.

    Returns the new path of the file.
    """
    file_name = os.path.basename(file_path)
    directory_path = os.path.join(directory_root, file_path)

    # Remove the file name from the path
    directory_path = os.path.dirname(directory_path)

    os.makedirs(directory_path, exist_ok=True)

    # Copy to the new directory (do not delete the original file, as it may be used elsewhere)
    new_path = os.path.join(directory_path, file_name)
    shutil.copy(file_path, new_path)
    return new_path

# TODO - Archive temporary directory from dependency 
# TODO - Create a function to redefine namespace of a module so that it can be imported from a different directory
def archive_directory(directory: str, archive_path: str, archive_type: str = "zip") -> str:
    """
    Archive a directory to an archived file.

    Args:
    - directory (str): The path to the directory.
    - archive_path (str): The path to the archive.
    - archive_type (str): The type of archive to create.

    Returns the path to the archive.
    """
    shutil.make_archive(archive_path, archive_type, directory)
    shutil.move(f"{archive_path}.{archive_type}", archive_path)
    shutil.rmtree(directory)

    return archive_path
