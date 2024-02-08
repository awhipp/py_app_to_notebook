"""Test the build utilities."""

import os

from py2databricks.utilities.build_utils import build_temporary_directory, create_run_file
from py2databricks.utilities.dir_utils import path_to_module_name
from py2databricks.models.dependency_tree import DependencyTree


def test_build_temporary_directory_and_create_run_file(output_dependency_paths_ordered):
    """Test building a temporary directory and creating a run file."""
    # ARRANGE
    dependency_tree: DependencyTree = DependencyTree(entrypoint=f"sample_application{os.sep}app.py")

    # ACT
    temporary_directory, files_created = build_temporary_directory(dependency_tree=dependency_tree)
    
    run_file = create_run_file(dependency_tree=dependency_tree, temporary_directory=temporary_directory)
    output_dependency_paths_ordered.append(run_file)

    # ASSERT
    assert files_created + 1 == len(output_dependency_paths_ordered)
    
    # Recursively get all files in the directory
    files = []
    for root, _, filenames in os.walk(temporary_directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # Add py2dbrx_importer.py to start of list
    output_dependency_paths_ordered.insert(0, "py2dbrx_importer.py")

    # Ensure the files are as expected
    for created_file in files:
        assert created_file.replace(f"{temporary_directory}{os.sep}", "") in output_dependency_paths_ordered

    assert run_file == "execute_application.py"

    with open(f"{temporary_directory}{os.sep}execute_application.py", "r", encoding="utf-8") as run_import_file:
        lines = run_import_file.readlines()
        idx = 1
        
        assert lines[0] == "# Databricks notebook source\n"
        for dependency in output_dependency_paths_ordered:
            dependency = dependency.replace(".py", "").replace("\\", "/")
            if dependency == "py2dbrx_importer":
                assert lines[idx] == "# COMMAND ----------\n"
                assert lines[idx + 1] == f"# MAGIC %run ./{dependency}\n"
                idx += 2
            elif dependency == "execute_application":
                continue
            else:
                assert lines[idx] == "# COMMAND ----------\n"
                assert lines[idx + 1] == "file_uuid = define_checkpoint()\n"
                assert lines[idx + 2] == "# COMMAND ----------\n"
                assert lines[idx + 3] == f"update_modules_from_checkpoint(file_uuid, '{path_to_module_name(dependency)}')\n"
                assert lines[idx + 4] == "# COMMAND ----------\n"
                assert lines[idx + 5] == f"# MAGIC %run ./{dependency}\n"
                idx += 6