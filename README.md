# amati

amati is designed to validate that a file conforms to [OpenAPI Specification](https://spec.openapis.org/oas/v3.1.1.html) (OAS).

Currently a proof of concept.

## Name

"Amati" means to observe in Malay, especially with attention to detail. It's also one of the plurals of beloved or favourite in Italian.

## Architecture

amati uses Pydantic, especially the validation, and `Typing` to construct the entire OAS as a single data type. Passing a dictionary to the top-level data type runs all the validation in the Pydantic models constructing a single set of inherited classes and datatypes that validate that the API specification is accurate.

Where the specification conforms, but relies on implementation-defined behavior (e.g. [data type formats](https://spec.openapis.org/oas/v3.1.1.html#data-type-format)), a warning will be raised.

## Testing and formatting

This project uses:

* [Pytest](https://docs.pytest.org/en/stable/) as a testing framework
* [PyLance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) on strict mode for type checking
* [Pylint](https://www.pylint.org/) as a linter, using a modified version from [Google's style guide](https://google.github.io/styleguide/pyguide.html)
* [Hypothesis](https://hypothesis.readthedocs.io/en/latest/index.html) for test data generation
* [mutmut](https://mutmut.readthedocs.io/en/latest/index.html) for mutation testing
* [Coverage](https://coverage.readthedocs.io/en/7.6.8/) on both the tests and code for test coverage
* [Black](https://black.readthedocs.io/en/stable/index.html) for automated formatting
* [isort](https://pycqa.github.io/isort/) for import sorting

It's expected that there are no errors, no surviving mutants and 100% of the code is reached and executed.

## Building

The project uses a [`pyproject.toml` file](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml) to determine what to build.

To install:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

To add the testing dependencies

```sh
pip install -e ".[dev]"
```

### Data

There are some scripts to create the data needed by the project, for example, all the possible licences. If the data needs to be refreshed this can be done by running the contents of `/scripts`. You'll need to install the additional build dependencies to do so.

```sh
pip install -e ".[build]"
```




