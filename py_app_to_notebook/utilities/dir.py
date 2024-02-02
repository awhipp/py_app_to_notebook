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

    path: str
    module_name: str
    name: str
    dependencies: set

    def __init__(self, root: str, path: str, parent: str = ""):
        """From a file path, create a dependency object."""
        self.root = root
        self.path = path.replace('\\', os.sep).replace('/', os.sep)
        if parent == "":
            self.module_name = os.path.basename(path).replace('.py', '')
        else:
            self.module_name = parent + "." + os.path.basename(path).replace('.py', '')
        self.name = os.path.basename(path).replace('.py', '')
        self.dependencies = set()
        
        self.find_dependencies()

    def __str__(self):
        """String representation of the dependency."""
        return f"{self.module_name} ({self.path})"
    
    def print_dependency_tree(self, level: int = 1):
        """Print the dependency tree."""
        print(self)
        for dependency in self.dependencies:
            print("----" * level, end="")
            dependency.print_dependency_tree(level + 1)

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
                        self.dependencies.add(
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
                        self.dependencies.add(
                            Dependency(
                                root=self.root,
                                path=module_path,
                                parent=self.module_name)
                        )

        
if __name__ == '__main__':
    entry_point = 'queue_to_s3_sample/app.py'
    dep = Dependency(root='queue_to_s3_sample', path=entry_point)
    dep.print_dependency_tree()
