"""Just prints and returns an environment variable"""

from sample_application.utilities.environment.variables import generate_and_set_random_string, get_env_var

def print_and_return():
    """
    Print and return the environment variable
    """
    generate_and_set_random_string()

    random_string = get_env_var('RANDOM_STRING')

    print(f"String is: {random_string}")
    return random_string