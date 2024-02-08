"""Builds a dependency tree for a given Python file. Two classes:
- Dependency: The main class that builds the  dependency information for a given Python file. This class just has the module_name, path, parent, and children attributes.
- DependencyTree: A class that builds the dependency tree for a given Python file. This class creates a dependency tree of parents and children. It also has a method to get dependencies based on name."""

import os
import ast
from typing import Optional, Literal
from py_app_to_notebook.utilities.dir_utils import module_name_to_path, path_to_module_name


class Dependency():
    """Represents a module.
    
    Attributes:
    - root: The root of the module.
    - path: The path of the module.
    - module_name: The name of the module.
    - parent: The parent of the module.
    - children: The children of the module.
    """
    
    root: str
    path: str
    module_name: str
    parent: Optional["Dependency"] = None
    children: list["Dependency"] = []

    def __init__(self, path: str,  root: Optional[str] = None, parent: Optional["Dependency"] = None):
        """From a file path, create a dependency object."""  
        if root:
            self.root = root
        else:
            self.root = path.split(os.sep)[0]  
        if path is None:
            raise ValueError("Path is required.")

        self.path = path.replace('\\', os.sep).replace('/', os.sep)

        if os.path.exists(self.path) is False:
            raise FileNotFoundError(f"File not found: {self.path}")

        self.parent = parent

        # Define module name based on self.path
        self.module_name = path_to_module_name(self.path)

        self.children = []

        self.find_dependencies()
        super().__init__()

    def __str__(self):
        """String representation of the dependency."""
        return f"{self.module_name}"
    
    def str_rep_node_and_dependencies(self, level: int = 1) -> str:
        """Recursively retrieves the dependency tree as a text string."""
        tree = f"{self}\n"
        for dependency in self.children:
            tree += "----" * level
            tree += dependency.str_rep_node_and_dependencies(level + 1)

        return tree
    
    def list_all_module_paths(self) -> list:
        """Recursively retrieves all module paths as a list."""
        tree = [self.path]
        for dependency in self.children:
            subtree = dependency.list_all_module_paths()
            for sub in subtree:
                if sub not in tree:
                    tree.append(sub)

        return tree
    
    def find_minimal_dependencies(self, minimal_dependencies: list = []) -> list:
        """Recursively go to the bottom of the tree, and return dependencies in order from least to most dependent."""

        if self.path in minimal_dependencies:
            return minimal_dependencies
        
        for dependency in self.children:
            if dependency.path not in minimal_dependencies:
                new_dependencies = dependency.find_minimal_dependencies(minimal_dependencies)
                for new_dependency in new_dependencies:
                    if new_dependency not in minimal_dependencies:
                        minimal_dependencies.append(new_dependency)
        
        if self.path not in minimal_dependencies:
            minimal_dependencies.append(self.path)

        return minimal_dependencies

    def find_dependencies(self):
        """Finds the dependencies of the current module."""
        with open(self.path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=self.path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_path = module_name_to_path(alias.name)
                    if self.root in module_path:
                        try:
                            child = Dependency(
                                    root=self.root,
                                    path=module_path,
                                    parent=self
                            )
                            self.children.append(child)
                        except FileNotFoundError:
                            pass
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if module_name is not None:
                    module_path = module_name_to_path(module_name)
                    if self.root in module_path:
                        try:
                            child = Dependency(
                                    root=self.root,
                                    path=module_path,
                                    parent=self
                            )
                            self.children.append(child)
                        except FileNotFoundError:
                            pass

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