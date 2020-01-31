## Development

## Installation

This project uses pipenv as python management tool. Run the following command to install dependencies:

```
pipenv install --dev
```

## Test

Run the following command for the tests:

```
pipenv run pytest --cov=apps
```

## Pre-commit

Once you have the code ready, pre-commit will run some checks to make sure the code follows the format and the tests did not break. If you want to run the check for all files at any point, run:

```
pipenv run pre-commit run --all-files
```
