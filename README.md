# Generate Notebook Application

This python CLI generates a Databricks archive from a source application so that it can run in Databricks without needing to install a whl file on a cluster. This is useful for deploying applications to Databricks that are not part of the Databricks ecosystem, or for deploying applications that are not part of the Databricks ecosystem. It is also for users that do not have the ability to install packages on a Databricks cluster.

## CI/CD

* [![CLI Tests](https://github.com/awhipp/python_app_to_databricks/actions/workflows/cli_tests.yml/badge.svg)](https://github.com/awhipp/python_app_to_databricks/actions/workflows/cli_tests.yml) - The CLI is tested to ensure it works as expected.

* [![Sample App Tests](https://github.com/awhipp/python_app_to_databricks/actions/workflows/sample_app_tests.yml/badge.svg)](https://github.com/awhipp/python_app_to_databricks/actions/workflows/sample_app_tests.yml) - The sample application that is used to test the CLI, and is packaged and archived in a way to be deployed to Databricks or Jupyter (i.e. any notebook environment).

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

Build the databricks archive file

```bash
py2databricks build --entrypoint <entrypoint_module> --output_name databricks_archive.zip
```

Print the dependency tree for the application

```bash
py2databricks print_dependency_tree --entrypoint <entrypoint_module>
```