"""Utility functions for building the notebook from the app."""
import os

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

def create_run_file(entrypoint: str, temporary_directory: str = None) -> str:
    """Given minimal dependence order, generate a magic run file to import all modules in order

    Args:
        entrypoint (str): The path to the entrypoint of the app.

    Returns:
        str: The path to the run file.
    """

    dependency_tree: DependencyTree = DependencyTree(entrypoint=entrypoint)

    # Get the dependencies list
    dependency_paths = dependency_tree.list_dependencies_in_order()
    
    if temporary_directory is None:
        temporary_directory = build_temporary_directory(entrypoint=entrypoint)

    # Run file takes the following pattern
    # 1. New Line with `# Command ----------`
    # 2. New line with run command in format `# MAGIC %run module_path`
    run_import_file_path = f"{temporary_directory}{os.sep}import_run.py"
    with open(run_import_file_path, "w", encoding="utf-8") as run_import_file:
        for path in dependency_paths:
            run_import_file.write("# Command ----------\n")
            
            # Check if path starts with a dot and os.sep
            if not path.startswith(f".{os.sep}"):
                path = f".{os.sep}" + path

            run_import_file.write(f"# MAGIC %run {path}\n")
    
    return run_import_file_path.replace(f"{temporary_directory}{os.sep}", "")
