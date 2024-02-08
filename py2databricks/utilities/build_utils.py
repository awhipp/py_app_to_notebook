"""Utility functions for building the notebook from the app."""
import os
import inspect

from py2databricks.models.dependency_tree import DependencyTree

from py2databricks.utilities.dir_utils import create_temporary_directory, move_file_to_directory, path_to_module_name

import py2databricks.module_importer.py2dbrx_importer as py2dbrx_importer

def build_temporary_directory(dependency_tree: DependencyTree) -> str:
    """
    Create a temporary directory to build the notebook.

    Args:
    - entrypoint (str): The path to the entrypoint of the app.

    Returns:
    - str: The path to the temporary directory.
    """

    # Create a temporary directory
    temporary_directory = create_temporary_directory()

    # Get the dependencies list
    dependency_paths = dependency_tree.list_all_module_paths()

    # Move the files to the temporary directory
    for path in dependency_paths:
        move_file_to_directory(path, temporary_directory)

    # Add py2dbrx_importer.py to the temporary directory
    with open(f"{temporary_directory}{os.sep}py2dbrx_importer.py", "w", encoding="utf-8") as py2dbrx_importer:
        py2dbrx_importer.write(get_importer_code())

    return temporary_directory, len(dependency_paths)

def get_importer_code() -> str:
    """Get the header for the importer code."""
    return inspect.getsource(py2dbrx_importer)

def create_run_file(dependency_tree: DependencyTree, temporary_directory: str) -> str:
    """Given minimal dependence order, generate a magic run file to import all modules in order

    Args:
        entrypoint (str): The path to the entrypoint of the app.

    Returns:
        str: The path to the run file.
    """

    # Get the dependencies list
    dependency_paths = dependency_tree.list_dependencies_in_order()


    # Run file takes the following pattern
    # 0. Adds the header from run_file_header.py so allow imports to run and fake modules to be created
    # 1. New Line with `# Command ----------`
    # 2. New line with run command in format `# MAGIC %run module_path`
    run_import_file_path = f"{temporary_directory}{os.sep}execute_application.py"
    with open(run_import_file_path, "w", encoding="utf-8") as run_import_file:
        run_import_file.write("# Databricks notebook source\n")
        run_import_file.write("# COMMAND ----------\n")
        run_import_file.write("# MAGIC %run ./py2dbrx_importer\n")

        for path in dependency_paths:

            # Define file checkpoint
            run_import_file.write("# COMMAND ----------\n")
            run_import_file.write("file_uuid = define_checkpoint()\n")

            # Update modules from checkpoint
            run_import_file.write("# COMMAND ----------\n")

            # Get module name from path
            module_name = path_to_module_name(path=path)
            # Remove dots from start
            while module_name.startswith('.'):
                module_name = module_name[1:]
        
            run_import_file.write(f"update_modules_from_checkpoint(file_uuid, '{module_name}')\n")
            
            # Define magic run command
            run_import_file.write("# COMMAND ----------\n")
            
            # Check if path starts with a dot and os.sep
            if not path.startswith(f".{os.sep}"):
                path = f"./{path}"

            run_path = path.replace('.py', '').replace('\\','/')
            run_import_file.write(f"# MAGIC %run {run_path}\n")
    
    return run_import_file_path.replace(f"{temporary_directory}{os.sep}", "")
