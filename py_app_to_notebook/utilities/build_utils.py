"""Utility functions for building the notebook from the app."""

from py_app_to_notebook.utilities.dependency import Dependency

from py_app_to_notebook.utilities.dir_utils import create_temporary_directory, move_file_to_directory

def build_temporary_directory(entrypoint: str) -> str:
    """
    Create a temporary directory to build the notebook.

    Args:
    - entrypoint (str): The path to the entrypoint of the app.

    Returns:
    - str: The path to the temporary directory.
    """
    
    dependency: Dependency = Dependency(path=entrypoint)

    # Create a temporary directory
    temporary_directory = create_temporary_directory()

    # Get the dependencies list
    dependencies = dependency.dependency_tree_as_list()

    # Move the files to the temporary directory
    for dep in dependencies:
        move_file_to_directory(dep, temporary_directory)

    return temporary_directory, len(dependencies)