"""This is a module that allows you to get or set environment variables."""


import os
import random

from sample_application.utilities.generators.randoms import generate_random_string

def get_env_var(var_name: str) -> str:
    """
    Get an environment variable
    """
    return os.environ.get(var_name, None)

def set_env_var(var_name: str, var_value: str) -> None:
    """
    Set an environment variable
    """
    os.environ[var_name] = var_value
    return None

def generate_and_set_random_string() -> None:
    """
    Generate a random string and set it as an environment variable
    """
    random_str = generate_random_string(
        length = random.randint(100, 200)
    )
    set_env_var('RANDOM_STRING', random_str)

def get_random_string() -> str:
    """
    Get the random string from the environment variables
    """
    return get_env_var('RANDOM_STRING')