"""Test the build utilities."""

import os
from py_app_to_notebook.utilities.build_utils import build_temporary_directory, create_run_file


def test_build_temporary_directory_and_create_run_file(output_dependency_paths_ordered):
    """Test building a temporary directory and creating a run file."""

    # ACT
    temporary_directory, files_created = build_temporary_directory(f'queue_to_s3_sample{os.sep}app.py')
    
    run_file = create_run_file(f'queue_to_s3_sample{os.sep}app.py', temporary_directory=temporary_directory)
    output_dependency_paths_ordered.append(run_file)

    # ASSERT
    assert files_created + 1 == len(output_dependency_paths_ordered)
    
    # Recursively get all files in the directory
    files = []
    for root, _, filenames in os.walk(temporary_directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # Ensure the files are as expected
    for created_file in files:
        assert created_file.replace(f"{temporary_directory}{os.sep}", "") in output_dependency_paths_ordered

    assert run_file == "import_run.py"

    with open(f"{temporary_directory}{os.sep}import_run.py", "r", encoding="utf-8") as run_import_file:
        lines = run_import_file.readlines()
        for i, line in enumerate(lines):
            if i % 2 == 0:
                assert line == "# Command ----------\n"
            else:
                assert line == f"# MAGIC %run .{os.sep}{output_dependency_paths_ordered[i // 2]}\n"

        
    # Recursively delete any empty folders and files
    for root, dirs, files in os.walk(temporary_directory, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))