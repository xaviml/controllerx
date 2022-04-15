## Contributing to ControllerX

## Installation

This project uses pipenv as python management tool. Run the following commands to install dependencies and hooking up the pre-commit to git

```
pipenv install --dev --python python3.7
pipenv shell
pre-commit install
```

_Note: I recommend working with Python 3.7 since is the minimum version supported_

## Adding a new controller

New controllers need to be added into the `apps/controllerx/devices/` and you will need to define the mapping for the integration you are adding support to.

Also, the controller will need to be added to the documentation. You will need to create:

- YAML file in `docs/_data/controllers`
- MarkDown file in `docs/controllers`
- JPEG image in `docs/assets/img`

The name of the files should be the model of the controller. For example, if the device model is `E1743`, then the name of the files should be: `E1743.{yaml, md, jpeg}`. You can easily find the model in the [Zigbee2MQTT supported devices page](https://www.zigbee2mqtt.io/information/supported_devices.html).

The class name convention should be `Device Model + Type + Controller`. For example, for a new light controller for E1743, the class name should be `E1743LightController`. Take into account that there are some old controllers that do not follow this convention.

Note that this project will only accept the mapping that the original controller would follow with its original hub, or the closest behaviour we can get.

This is a [commit](https://github.com/xaviml/controllerx/commit/38ee4b03ac31bf966523cc63c0200567f912f201) of a complete example of adding a new device, it can be used as a reference.

## Imports

Run the following to fix imports order:

```shell
pipenv run isort apps/controllerx/ tests/
```

## Format

Run the following to fix formatting:

```shell
pipenv run black apps/controllerx/ tests/
```

## Typing

Run the following to check consistency in the typings:

```shell
pipenv run mypy apps/controllerx/ tests/
```

## Linting

Run the following to check for stylings:

```shell
pipenv run flake8 apps/controllerx/ tests/
```

## Test

Run the following command for the tests:

```shell
pipenv run pytest --cov=apps
```

or the following to get a report of the missing lines to be tested:

```shell
pytest --cov-report term-missing --cov=apps
```

## Pre-commit

Once you have the code ready, pre-commit will run some checks to make sure the code follows the format and the tests did not break. If you want to run the check for all files at any point, run:

```shell
pipenv run pre-commit run --all-files
```

## Commiting

You can use the tool `commitizen` to commit based in a standard. If you are in the virtual environment, you can run `cz commit` and answer the questions to commit.

If the commit adds new functionality or fixes something, please add the changes in the `RELEASE_NOTES.md` file.

## Documentation

[Install Jekyll](https://jekyllrb.com/docs/) and run the documentation locally with:

```shell
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
git fetch <username> <branch>
git checkout -b <username>-<branch> <username>/<branch>
```

Once the changes are commited, you can push with the following command:

```shell
git push <username> HEAD:<branch>
```

## Deployment

Thanks to the Azure Pipelines, we are able to deploy by just creating a new tag on git. Before proceding with new version bump, make sure to have all the changes for this release in the `RELEASE_NOTES.md` file.

We use `commitizen` to bump version. First, we might want to create a beta version from `dev` branch:

```shell
cz bump --no-verify --prerelease beta
git push origin HEAD --tags
```

_`--dry-run` can be used with `cz` command to double check the version to be created._

Once we are ready to create the final version, we need to merge to main branch with no fast forward:

```shell
git checkout main
git merge dev --no-ff
```

Finally, we can bump the version to the final one, and push tag:

```shell
cz bump --no-verify
git push origin HEAD --tags
```

_`--dry-run` can be used with `cz` command to double check the version to be created._

When a new tag is created, the CI will automatically generate a GitHub release with the changes for that release, and the release from the `RELEASE_NOTES.md` file.
