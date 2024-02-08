"""Test the build utilities."""

import os
from py_app_to_notebook.utilities.build_utils import build_temporary_directory, create_run_file

from py_app_to_notebook.utilities.dir_utils import path_to_module_name

from py_app_to_notebook.utilities.dependencies import DependencyTree


def test_build_temporary_directory_and_create_run_file(output_dependency_paths_ordered):
    """Test building a temporary directory and creating a run file."""
    # ARRANGE
    dependency_tree: DependencyTree = DependencyTree(entrypoint=f"queue_to_s3_sample{os.sep}app.py")

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

    # Add import_helper.py to start of list
    output_dependency_paths_ordered.insert(0, "import_helper.py")

    # Ensure the files are as expected
    for created_file in files:
        assert created_file.replace(f"{temporary_directory}{os.sep}", "") in output_dependency_paths_ordered

    assert run_file == "import_run.py"

    with open(f"{temporary_directory}{os.sep}import_run.py", "r", encoding="utf-8") as run_import_file:
        lines = run_import_file.readlines()
        idx = 0
        for dependency in output_dependency_paths_ordered:
            if dependency == "import_helper.py":
                assert lines[idx] == "# Command ----------\n"
                assert lines[idx + 1] == f"# MAGIC %run .{os.sep}{dependency}\n"
                idx += 2
            elif dependency == "import_run.py":
                continue
            else:
                assert lines[idx] == "# Command ----------\n"
                assert lines[idx + 1] == "file_uuid = define_checkpoint()\n"
                assert lines[idx + 2] == "# Command ----------\n"
                assert lines[idx + 3] == f"# MAGIC %run .{os.sep}{dependency}\n"
                assert lines[idx + 4] == "# Command ----------\n"
                assert lines[idx + 5] == f"update_modules_from_checkpoint(file_uuid, '{path_to_module_name(dependency)}')\n"
                idx += 6