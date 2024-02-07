"""Utility functions for building the notebook from the app."""
import os
import inspect

from py_app_to_notebook.utilities.dependencies import DependencyTree

from py_app_to_notebook.utilities.dir_utils import create_temporary_directory, move_file_to_directory, path_to_module_name

import py_app_to_notebook.files.import_helper as import_helper

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

    # Add import_helper.py to the temporary directory
    with open(f"{temporary_directory}{os.sep}import_helper.py", "w", encoding="utf-8") as import_helper_file:
        import_helper_file.write(get_run_file_header())

    return temporary_directory, len(dependency_paths)

def get_run_file_header() -> str:
    """Get the header for the run file."""
    return inspect.getsource(import_helper)

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
    # 0. Adds the header from run_file_header.py so allow imports to run and fake modules to be created
    # 1. New Line with `# Command ----------`
    # 2. New line with run command in format `# MAGIC %run module_path`
    run_import_file_path = f"{temporary_directory}{os.sep}import_run.py"
    with open(run_import_file_path, "w", encoding="utf-8") as run_import_file:
        run_import_file.write("# Command ----------\n")
        run_import_file.write(f"# MAGIC %run .{os.sep}import_helper.py\n")

        for path in dependency_paths:

            # Define file checkpoint
            run_import_file.write("# Command ----------\n")
            run_import_file.write("file_uuid = define_checkpoint()\n")

            # Define magic run command
            run_import_file.write("# Command ----------\n")
            
            # Check if path starts with a dot and os.sep
            if not path.startswith(f".{os.sep}"):
                path = f".{os.sep}" + path

            run_import_file.write(f"# MAGIC %run {path}\n")

            # Update modules from checkpoint
            run_import_file.write("# Command ----------\n")

            # Get module name from path
            module_name = path_to_module_name(path=path)
            # Remove dots from start
            while module_name.startswith('.'):
                module_name = module_name[1:]
        
            run_import_file.write(f"update_modules_from_checkpoint(file_uuid, '{module_name}')\n")
    
    return run_import_file_path.replace(f"{temporary_directory}{os.sep}", "")
