## Contributing to ControllerX

## Installation

This project uses pipenv as python management tool. Run the following commands to install dependencies and hooking up the pre-commit to git

```
pipenv install --dev
pipenv shell
pre-commit install
```


## Adding a new controller

New controllers need to be added into the `apps/controllerx/devices/` and you will need to define the mapping for the integration you are adding support to.

Note that this project will only accept the mapping that the original controller would follow with its original hub.

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

## Documentation

[Install Jekyll](https://jekyllrb.com/docs/) and run the documentation locally with:

```
cd docs
bundle install
bundle exec jekyll serve
```
