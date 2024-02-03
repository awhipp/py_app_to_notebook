"""
Directory utilities, specifically used to determine the dependencies of a Python app.
"""
import ast
import os

from typing import Optional

def module_name_to_path(module_name) -> str:
    """
    Convert a module name to a path.

    Args:
    - module_name (str): The name of the module.

    Returns:
    - str: The path to the module.
    """
    return module_name.replace('.', os.sep) + '.py'

class Dependency():
    """Represents a modules, its name and path"""

    root: str
    path: str
    module_name: str
    name: str
    dependencies: list

    def __init__(self, path: str,  root: Optional[str] = None, parent: str = ""):
        """From a file path, create a dependency object."""    
        if root:
            self.root = root
        else:
            self.root = path.split(os.sep)[0]

        if path is None:
            raise ValueError("Path is required.")

        self.path = path.replace('\\', os.sep).replace('/', os.sep)
        if parent == "":
            self.module_name = os.path.basename(path).replace('.py', '')
        else:
            self.module_name = parent + "." + os.path.basename(path).replace('.py', '')
        self.name = os.path.basename(path).replace('.py', '')
        self.dependencies = []
        
        self.find_dependencies()
        super().__init__()

    def __str__(self):
        """String representation of the dependency."""
        return f"{self.module_name} ({self.path})"
    
    def dependency_tree_as_string(self, level: int = 1) -> str:
        """Recursively retrieves the dependency tree as a text string."""
        tree = f"{self}\n"
        for dependency in self.dependencies:
            tree += "----" * level
            tree += dependency.dependency_tree_as_string(level + 1)

        return tree
   
    def find_dependencies(self):
        """
        Get the dependency tree of a Python file based on its imports.
        """

        with open(self.path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=self.path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_path = module_name_to_path(alias.name)
                    if self.root in module_path:
                        self.dependencies.append(
                            Dependency(
                                root=self.root,
                                path=module_path,
                                parent=self.module_name
                            )
                        )
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if module_name is not None:
                    module_path = module_name_to_path(module_name)
                    if self.root in module_path:
                        self.dependencies.append(
                            Dependency(
                                root=self.root,
                                path=module_path,
                                parent=self.module_name
                            )
                        )
