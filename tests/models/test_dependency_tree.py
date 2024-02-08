"""Tests the dependency tree class and by extension the dependency class."""

import os
from py2databricks.models.dependency_tree import DependencyTree
from py2databricks.models.dependency import Dependency

class TestDependencyTree():
    """Test the Dependency Tree class."""

    dependency_tree: DependencyTree = DependencyTree(entrypoint=f'sample_application{os.sep}app.py')

    def test_entrypoint_set(self):
        """Test the root is set."""
        assert self.dependency_tree.entrypoint == f'sample_application{os.sep}app.py'
        assert self.dependency_tree.root_dependency.root == 'sample_application'

    def test_dependency_tree_string(self, output_dependency_string):
        """Test the dependency tree string."""

        # ACT
        tree = self.dependency_tree.tree_as_string()

        # ASSERT
        assert tree == output_dependency_string

    def test_list_all_module_paths(self, output_dependency_paths):
        """Test the dependency module path list."""

        # ACT
        module_paths = self.dependency_tree.list_all_module_paths()

        # ASSERT
        assert module_paths == output_dependency_paths

    def test_build_tree_pointers(self, output_dependency_tree_keys):
        """Test the build tree pointers method."""

        # ASSERT
        for key, value in self.dependency_tree.nodes.items():
            assert key in output_dependency_tree_keys
            assert isinstance(value, Dependency)

    def test_list_dependencies_in_order(self, output_dependency_paths_ordered):
        """Test the list dependencies in order method."""
        ordered_dependencies_asc = self.dependency_tree.list_dependencies_in_order()
        assert ordered_dependencies_asc == output_dependency_paths_ordered

        ordered_dependencies_desc = self.dependency_tree.list_dependencies_in_order(order="descending")
        assert ordered_dependencies_desc == list(reversed(output_dependency_paths_ordered))

        