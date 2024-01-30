# Generate Notebook Application

This python CLI generates a notebook from a source application so that it can run in Databricks or Jupyter (i.e. most notebook environments).

## CI/CD

* [![CLI Tests](https://github.com/awhipp/py_app_to_notebook/actions/workflows/cli_tests.yml/badge.svg)](https://github.com/awhipp/py_app_to_notebook/actions/workflows/cli_tests.yml) - The CLI is tested to ensure it works as expected.

* [![Sample App Tests](https://github.com/awhipp/py_app_to_notebook/actions/workflows/sample_app_tests.yml/badge.svg)](https://github.com/awhipp/py_app_to_notebook/actions/workflows/sample_app_tests.yml) - The sample application that is used to test the CLI, and is packaged and archived in a way to be deployed to Databricks or Jupyter (i.e. any notebook environment).

## Installation

Install dependencies with poetry:

```bash
poetry install
```

## Testing

Beyond dependencies and a sample application nothing further is needed.

```bash
poetry run pytest
```


## Usage

WIP - Command documentation to come
