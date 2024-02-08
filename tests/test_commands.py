# tests/test_commands.py
import os
from click.testing import CliRunner
from py2databricks.commands import print_dependency_tree, build

def test_print_dependency_tree(output_dependency_string):
    """Ensure the print_dependency_tree command works. Tests output as well."""
    runner = CliRunner()
    # Invoke print_dependency_tree with the entrypoint option
    result = runner.invoke(print_dependency_tree, ["--entrypoint", f"queue_to_s3_sample{os.sep}app.py"])
    assert result.exit_code == 0
    assert result.output == f"{output_dependency_string}\n" # Add newline to match expected output

def test_build():
    """Ensure the build command works. Tests output as well."""
    runner = CliRunner()
    # Check if relative path exists
    assert os.path.exists(f".{os.sep}queue_to_s3_sample{os.sep}app.py")

    result = runner.invoke(build, ["--entrypoint", f".{os.sep}queue_to_s3_sample{os.sep}app.py", "--output_name", f".{os.sep}queue_to_s3_archive.zip"])
    assert result.exit_code == 0
    assert result.output == f"""Building notebook archive (.{os.sep}queue_to_s3_archive.zip) for .{os.sep}queue_to_s3_sample{os.sep}app.py...
Generated notebook archive at .{os.sep}queue_to_s3_archive.zip.
"""
    assert os.path.exists(f".{os.sep}queue_to_s3_archive.zip")

    # Cleanup
    os.remove(f".{os.sep}queue_to_s3_archive.zip")


