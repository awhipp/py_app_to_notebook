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
    print("Generating Random Number and setting it in the environemnt.")
    return_value = print_and_return() == os.environ.get("RANDOM_STRING", None)
    print(f"Confirmed Environment Set: {return_value}")

if __name__ == "__main__":
    print("""This is executing multiple notebooks in a Databricks environment.
Further there are dynamically defined modules being run here. You can:
          1. Run the `app.py` file to see the output.
          2. Import from other modules (i.e. notebooks) and run them.
          3. Support for aliased imports.
          4. Definitely a beta solution, but gets around the need for installing WHL files on Databricks.
          5. Likely to be slow, but it works, and is a good starting point for a more robust solution.
""")
    
    main()
