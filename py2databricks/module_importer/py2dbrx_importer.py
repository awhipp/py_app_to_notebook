"""This module is used to define a checkpoint and update the checkpoint between %run calls.

This module is not meant to be run directly.
It is meant to be used in a Jupyter Notebook environment.
It is used to define a checkpoint and update the checkpoint between %run calls.

Example Execution--------------------------
file_uuid = define_checkpoint()
%run ./path/to/file.py
update_modules_from_checkpoint(file_uuid, "example.module")
import example.module
"""

from types import ModuleType
from typing import Any

import logging

# Set up logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "[%(levelname)s][%(name)s:%(funcName)s:%(lineno)d]:%(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    logger.setLevel(LOG_LEVEL)
except Exception as _:
    logger.setLevel(logging.INFO)

class FakeModule(ModuleType):
    """This is a fake module to be used in sys.modules

    Args:
        ModuleType: The base class for all module objects in Python
    """
    def __getattr__(self, key: str) -> Any:
        if key == '__path__':
            return []
        elif key == '__file__':
            return ""
        try:
            return globals()[key]
        except KeyError:
            return globals()[f"{self.__name__}.{key}"]

def define_checkpoint():
    """Define a checkpoint for the current state of the globals() and return the file_uuid where its stored."""
    from uuid import uuid4
    file_uuid = str(uuid4())
    globals()[f"checkpoint-{file_uuid}"] = dict(globals())
    return file_uuid

def get_all_module_chunks(modules: list) -> str:
    """Generator which provides all the module chunks from a list of modules.

    i.e. ['test', 'module', 'example'] -> ['test', 'test.module', 'test.module.example']
    """
    for idx, _ in enumerate(modules):
        yield '.'.join(modules[:idx+1])

def update_modules_from_checkpoint(file_uuid: dict, module_name: str):
    """Update the modules from the checkpoint in globals()."""
    import sys

    if f"checkpoint-{file_uuid}" not in globals():
        raise KeyError(f"Checkpoint {file_uuid} not found in globals. Likely already imported.")
    
    checkpoint: dict = globals()[f"checkpoint-{file_uuid}"]
    del globals()[f"checkpoint-{file_uuid}"]

    # Add module_name to globals and sys.modules if not exists
    split_module_name = module_name.split('.')
    previous_modules = get_all_module_chunks(split_module_name)

    # Add all the modules to sys.modules
    for module in previous_modules:
        if module not in sys.modules:
            logger.debug(f"Adding Empty {module} to sys.modules")
            sys.modules[module] = FakeModule(module, f"Fake module for {module}")

    new_checkpoint = dict(globals())
    for key in new_checkpoint:
        if key not in checkpoint:            
            # Add it to sys.modules
            logger.debug(f"Adding {module_name} and {module_name}.{key} to sys.modules")

            sys.modules[module_name].__dict__[key] = new_checkpoint[key]
            sys.modules[f"{module_name}.{key}"] = FakeModule(f"{module_name}.{key}", new_checkpoint[key])
            globals()[f"{module_name}.{key}"] = new_checkpoint[key]

            # Remove old from globals
            del globals()[key]


if __name__ == "__main__":
    print("Importer is ready.")