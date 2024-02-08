from setuptools import setup, find_packages

# TODO Untested - Tech debt

setup(
    name='py2databricks',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        # Add any other dependencies here
    ],
    entry_points='''
        [console_scripts]
        your-cli-app=py2databricks.cli:cli
    ''',
    author='Alexander Whipp',
    description='This python CLI generates a notebook from a source application so that it can run in Databricks or Jupyter (i.e. most notebook environments).',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
