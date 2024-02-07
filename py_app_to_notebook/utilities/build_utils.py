"""Utility functions for building the notebook from the app."""

from py_app_to_notebook.utilities.dependencies import DependencyTree

from py_app_to_notebook.utilities.dir_utils import create_temporary_directory, move_file_to_directory

def build_temporary_directory(entrypoint: str) -> str:
    """
    Create a temporary directory to build the notebook.

    Args:
    - entrypoint (str): The path to the entrypoint of the app.

    Returns:
    - str: The path to the temporary directory.
    """
    
    dependency_tree: DependencyTree = DependencyTree(entrypoint=entrypoint)

    # Create a temporary directory
    temporary_directory = create_temporary_directory()

    # Get the dependencies list
    dependency_paths = dependency_tree.list_all_module_paths()

    # Move the files to the temporary directory
    for path in dependency_paths:
        move_file_to_directory(path, temporary_directory)

    return temporary_directory, len(dependency_paths)

# TODO Create a function to go from a list of dependencies to a list of minimal dependencies
def sorted_minimal_dependency_list(entrypoint: str) -> tuple[list[str], dict[str, int]]:
    raise NotImplementedError("This function is not yet implemented.")