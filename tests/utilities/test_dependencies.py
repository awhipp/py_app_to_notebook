"""Directory utilities, specifically used to determine the dependencies of a Python app."""
import os
from py_app_to_notebook.utilities.dependencies import DependencyTree, Dependency

class TestDependency():
    """Test the Dependency class."""

    dependency_tree: DependencyTree = DependencyTree(entrypoint=f'queue_to_s3_sample{os.sep}app.py')

    def test_entrypoint_set(self):
        """Test the root is set."""
        assert self.dependency_tree.entrypoint == f'queue_to_s3_sample{os.sep}app.py'
        assert self.dependency_tree.root_dependency.root == 'queue_to_s3_sample'

    def test_dependency_tree_string(self, output_dependency_string):
        """Test the dependency tree string."""

        # ACT
        tree = self.dependency_tree.tree_as_string()

        # ASSERT
        assert tree == output_dependency_string

    def test_list_all_module_paths(self, output_dependency_paths):
        """Test the dependency module path list."""

        # ACT
        tree = self.dependency_tree.list_all_module_paths()

        # ASSERT
        assert tree == output_dependency_paths

    def test_build_tree_pointers(self, output_dependency_tree_keys):
        """Test the build tree pointers method."""

        # ASSERT
        for key, value in self.dependency_tree.nodes.items():
            assert key in output_dependency_tree_keys
            assert isinstance(value, Dependency)