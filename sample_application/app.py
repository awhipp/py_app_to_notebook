"""
This is a sample application that:
1. Generates a random number from a utility package
2. Using that number it generates a random string
4. This string is the stored in the environment variable `RANDOM_STRING`. 
5. A final module reads this environment variable and prints it to the console.
"""
import os
from sample_application.utilities.driver import print_and_return

def main():
    """Main function
    """
    return_value = print_and_return() == os.environ.get("RANDOM_STRING", None)
    print(f"Confirmed Environment Set: {return_value}")
