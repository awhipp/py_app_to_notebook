"""Builds a dependency tree for a given Python file. Two classes:
- Dependency: The main class that builds the  dependency information for a given Python file. This class just has the module_name, path, parent, and children attributes.
- DependencyTree: A class that builds the dependency tree for a given Python file. This class creates a dependency tree of parents and children. It also has a method to get dependencies based on name."""

import os

from typing import Literal

from py2databricks.models.dependency import Dependency

class DependencyTree():
    """Represents a dependency tree.

    """

    entrypoint: str
    root_dependency: Dependency
    nodes: dict[str, Dependency]

    def __init__(self, entrypoint: str):
        """Create a dependency tree."""
        self.entrypoint = entrypoint
        self.nodes = {}
        self.root_dependency = Dependency(path=self.entrypoint)
        self.build_tree_pointers(self.root_dependency)

    def build_tree_pointers(self, node: Dependency):
        """Recursively builds a dictionary of nodes to quickly access the dependency tree."""
        if node.module_name not in self.nodes:
            self.nodes[node.module_name] = node

        for child in node.children:
            self.build_tree_pointers(child)

    def tree_as_string(self) -> str:
        """Returns the dependency tree as a string."""
        return self.root_dependency.str_rep_node_and_dependencies()
    
    def list_all_module_paths(self) -> list:
        """Returns all the module paths in the dependency tree."""
        return self.root_dependency.list_all_module_paths()
        
    def list_dependencies_in_order(self, order: Literal["descending", "ascending"] = "ascending") -> list:
        """Returns the dependencies in order based on the order parameter."""
        
        dependencies: list = self.root_dependency.find_minimal_dependencies()

        ## These are two test issues TODO fix
        # No dependencies should start with a .{os.sep}
        dependencies = [dep.replace(f".{os.sep}", "") for dep in dependencies]
        # Ensure unique without messing with order
        dependencies = list(dict.fromkeys(dependencies))

        if order == "descending":
            dependencies = list(reversed(dependencies))

        return dependencies