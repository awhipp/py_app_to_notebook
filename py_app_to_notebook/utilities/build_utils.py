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

# TODO - Definitely need to define a tree structure and work up it. Longer term goal.
def sorted_minimal_dependency_list(entrypoint: str) -> tuple[list[str], dict[str, int]]:
    """
    Get the dependencies of the app from least dependent to most dependent.

    Args:
    - entrypoint (str): The path to the entrypoint of the app.

    Returns:
    - list: The dependencies from least dependent to most dependent.
    - dict: The dependency dictionary.
    """
    dependency: Dependency = Dependency(path=entrypoint)

    # Get the dependencies list
    dependency_dictionary: dict[str, int] = dependency.dependency_count_search()

    # Sort the dependencies by the count, and return as an ordered list
    sorted_dependency_count: str = [k for k, v in sorted(dependency_dictionary.items(), key=lambda item: item[1])]

    return sorted_dependency_count, dependency_dictionary