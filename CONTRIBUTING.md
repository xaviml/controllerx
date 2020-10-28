## Contributing to ControllerX

## Installation

This project uses pipenv as python management tool. Run the following commands to install dependencies and hooking up the pre-commit to git

```
pipenv install --dev --python python3.6
pipenv shell
pre-commit install
```

_Note: I recommend working with Python 3.6 since is the minimum version supported_

## Adding a new controller

New controllers need to be added into the `apps/controllerx/devices/` and you will need to define the mapping for the integration you are adding support to.

Note that this project will only accept the mapping that the original controller would follow with its original hub.

## Typing

Run the following to check consistency in the typings:

```
pipenv run mypy apps/controllerx
```

## Linting

Run the following to check for stylings:

```
pipenv run flake8 apps/controllerx
```

## Test

Run the following command for the tests:

```
pipenv run pytest --cov=apps
```

or the following to get a report of the missing lines to be tested:

```
pytest --cov-report term-missing --cov=apps
```

## Pre-commit

Once you have the code ready, pre-commit will run some checks to make sure the code follows the format and the tests did not break. If you want to run the check for all files at any point, run:

```
pipenv run pre-commit run --all-files
```

## Commiting

You can use the tool `commitizen` to commit based in a standard. If you are in the virtual environment, you can run `cz commit` and answer the questions to commit.

## Documentation

[Install Jekyll](https://jekyllrb.com/docs/) and run the documentation locally with:

```
cd docs
bundle install
bundle exec jekyll serve
```

## Pull Request

Feel free to open a PR on GitHub. When submitting the PR several points will be checked:

- Testing (with pytest)
- Linting (with flake8)
- Typing (with mypy)
- Formatting (with black)

## How to change someone else's PR code

If you have the permission to change code from the source branch of the PR, then you can do the following to change it. First, you will need to add the remote:

```shell
git remote add <username> git@github.com:<username>/controllerx.git
```

Then you will need to fetch, create and checkout the branch:

```shell
git fetch <username> <remote-branch>
git checkout -b <username>-<remote-branch> <username>/<remote-branch>
```

## Deployment

Thanks to the Azure Pipelines, we are able to deploy by just creating a new tag on git. So first, we will need to bump version with `commitizen` by running the following line in the `master` branch:

```
cz bump --no-verify
```

`--prerelease beta` tag can be added to create a pre-release. Note that you can also add `--dry-run` to see which version will bump without commiting anything. Then, we can directly push the tags:

```
git push origin master --tags
```

This will automatically generate a GitHub release with the changes for that release.
