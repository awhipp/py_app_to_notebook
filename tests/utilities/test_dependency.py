"""Directory utilities, specifically used to determine the dependencies of a Python app."""
import os
from py_app_to_notebook.utilities.dependency import Dependency

class TestDependency():
    """Test the Dependency class."""

    dependency: Dependency = Dependency(path=f'queue_to_s3_sample{os.sep}app.py')

    def test_root_set(self):
        """Test the root is set."""
        assert self.dependency.root == 'queue_to_s3_sample'

    def test_dependency_tree_string(self, output_dependency_tree):
        """Test the dependency tree string."""

        # ACT
        tree = self.dependency.dependency_tree_as_string()

        # ASSERT
        assert tree == output_dependency_tree

    def test_dependency_tree_list(self, output_dependency_tree_list):
        """Test the dependency tree list."""

        # ACT
        tree = self.dependency.dependency_tree_as_list()

        # ASSERT
        assert tree == output_dependency_tree_list