"""
Directory utilities, specifically used to determine the dependencies of a Python app.
"""
import ast
import os

def is_internal_dependency(module_name, root_folder):
    """
    Check if a module is an internal dependency (part of the source codebase).

    Args:
    - module_name (str): The name of the module.
    - root_folder (str): The root folder containing Python files.

    Returns:
    - bool: True if the module is internal, False otherwise.
    """
    module_path = module_name.replace('.', os.sep)
    return os.path.exists(module_path + '.py') or os.path.exists(module_path)

def get_dependencies(file_path: str, root_folder: str):
    """
    Get the dependency tree of a Python file based on its imports.

    Args:
    - file_path (str): The path to the Python file.
    - root_folder (str): The root folder containing Python files.

    Returns:
    - set: A set containing the names of the modules the file depends on.
    """
    dependencies = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if is_internal_dependency(alias.name, root_folder):
                    dependencies.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            if module_name is not None and is_internal_dependency(module_name, root_folder):
                dependencies.add(module_name)

    return dependencies

def print_dependency_tree(dependency_tree: dict[str, str], node: str, indentation=""):
    result = f"{indentation}- {os.path.basename(node)}"
    print(dependency_tree)
    print("---- " + node)
    for dependency in dependency_tree[node]:
        result += "\n" + print_dependency_tree(dependency, indentation + "  ")
    return result

def analyze_dependency_tree(root_folder: str, skip_tests: bool = True):
    """
    Analyze the dependency tree of all Python files in a given folder.

    Args:
    - root_folder (str): The root folder containing Python files.
    - skip_tests (bool): Whether to skip test files.

    Returns:
    - dict: A dictionary where keys are Python file names, and values are sets
            containing the names of the modules each file depends on.
    """
    dependency_tree = {}

    for root, dirs, files in os.walk(root_folder):
        for file_name in files:
            if skip_tests and 'test' in file_name.lower():
                continue
            if "site-packages" in root or ".venv" in root or "__init__" in file_name:
                continue
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                dependencies = get_dependencies(file_path, root_folder)
                dependency_tree[file_path] = dependencies

    return dependency_tree

if __name__ == '__main__':
    # Example usage:
    root_folder_path = 'queue_to_s3_sample/'
    dependency_tree = analyze_dependency_tree(root_folder_path)

    # Print 
    tree_representation = ""
    for node in dependency_tree:
        tree_representation += print_dependency_tree(dependency_tree, node) + "\n"

    print(
        tree_representation.strip()
    )