Chart Book
==========


[![PyPI - Version](https://img.shields.io/badge/TestPyPI-v0.0.4-blue?logo=pypi)](https://test.pypi.org/project/chartbook)
[![PyPI - Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue?logo=python)](https://test.pypi.org/project/chartbook)
[![Tests](https://github.com/jmbejara/chartbook/actions/workflows/test.yml/badge.svg)](https://github.com/jmbejara/chartbook/actions/workflows/test.yml)

A Python package for generating a centralized chart and analytics catalog, and maintaining a series of reproducible analytics pipelines. 


## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [License](#license)
- [Development](#development)


## Installation

```console
pip install git+https://github.com/jmbejara/chartbook@main
```
or add it to your requirements.txt file:

```
chartbook @ git+https://github.com/jmbejara/chartbook@main
```



## Quick Start

```console
chartbook generate 
```
or

```console
chartbook generate --pipeline-theme chartbook
```

## Usage Guide

TODO


I recommend using the Hatch shell environment to install the package.
```
hatch shell
pip install -e .
```

## License

All rights reserved.

## Development

This package uses [Hatch](https://hatch.pypa.io/) for development and package management. Here's how to set up your development environment:

1. First, install Hatch if you haven't already:
```console
pip install hatch
```

2. Clone the repository:
```console
git clone https://github.com/jmbejara/chartbook
cd chartbook
```

3. Create and activate a development environment:
```console
hatch shell
```

4. Run the included example pipeline:
```console
chartbook generate --pipeline-theme chartbook ./docs
```




This will automatically install all dependencies and the package in editable mode.

### Running Tests

The package uses pytest for testing. To run tests:

```console
hatch test
```

You can also run tests with coverage:
```console
hatch test --cover
```

For verbose output:
```console
hatch test -v
```

### Formatting and Linting

You can use `hatch fmt` to format your Python code. This uses Ruff under the hood. 

```console
hatch fmt
```
Hatch's formatter supports configuration options such as quote style, indent style, and line width through the project's configuration file. However, it's worth noting that if you need to both sort imports and format code, you'll need to run two commands:

```console
hatch fmt --check  # for just checking formatting
```

### Development Tips

- The development environment created by `hatch shell` includes all necessary dependencies
- No need to manually install in editable mode (`pip install -e .`) as Hatch handles this
- Any changes you make to the source code will be immediately reflected when you import the package
- To exit the Hatch shell environment, simply type `exit`


## Notes for potentially using uv


```
rm uv.lock && uv sync && uv run chartbook generate --pipeline-theme pipeline ./docs   
uv run --directory /Users/jbejarano/GitRepositories/chartbook/chartbook chartbook generate --pipeline-theme pipeline ./docs

```
```
pip uninstall chartbook
pip install --force-reinstall git+https://github.com/jmbejara/chartbook.git
chartbook generate --pipeline-theme pipeline ./docs
```
or
```
chartbook generate --pipeline-theme chartbook ./docs
```

```
uv pip install --force-reinstall git+https://github.com/jmbejara/chartbook.git
chartbook generate --pipeline-theme pipeline ./docs

uvx --from git+https://github.com/jmbejara/chartbook chartbook generate --pipeline-theme pipeline ./docs
```
or
```
uv run chartbook generate --pipeline-theme pipeline ./docs
```

```
ipython --pdb src/chartbook/cli.py -- generate --pipeline-theme chartbook ./docs
```