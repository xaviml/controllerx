## Contributing to ControllerX

## Installation

This project uses poetry as python management tool. Run the following commands to install dependencies and hooking up the pre-commit to git

```
poetry install
poetry shell
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

## Styling

This repository uses [pre-commit](https://pre-commit.com/) which allows us to keep some code standards by using several tools (isort, black, mypy, flake8, etc). For more detail check `.pre-commit-config.yaml` file.

The following command can be executed to run all checkers for all files:

```shell
pre-commit run --all-files
```

If you want to run it for ust the staged files:

```shell
pre-commit run
```

If `pre-commit` was installed into git hooks (`pre-commit install`), it will run the checkers before the commit.

## Test

Run the following command for the tests:

```shell
pytest
```

or the following to get a report of the missing lines to be tested:

```shell
pytest --cov-report term-missing --cov=apps
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

Feel free to open a PR on GitHub. It would be appreciated if the CI passes (pre-commit and pytest).

## Run code with AppDaemon

### Docker

This is the easiest option to run your code with AppDaemon and try your changes. First, you need to add `apps.yaml` in the root of the project with the ControllerX configuration. For example:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
```

Second, you will need an HA Long-Lived Access Tokens (`YOUR_HA_TOKEN`) which you can get at `/profile` from your HA instance.

Then, you can run the following:

```shell
docker run \
-v $PWD/apps/controllerx:/usr/src/app/conf/apps/controllerx \
-v $PWD/apps.yaml:/usr/src/app/conf/apps/apps.yaml \
--rm -e DASH_URL=http://127.0.0.1:5050 \
-e HA_URL="http://YOUR_HA_IP:8123" \
-e TOKEN="YOUR_HA_TOKEN" \
acockburn/appdaemon:latest
```

This will start AppDaemon with the apps on the `apps.yaml`. Note that this will not work with `mqtt` integration or `z2m` with `listen_to: mqtt`. [This PR in AppDaemon](https://github.com/AppDaemon/appdaemon/pull/1454) fixes the use of `MQTT` with docker.

### Samba addon

Install `Samba share` addon in Home Assistant, so you can connect to HA folder structure from your computer. Then, you can just copy `apps/controllerx` on `/config/appdaemon/apps/`. When done, you should be able to find `controllerx.py` in `/config/appdaemon/apps/controllerx/controllerx.py`. Then, you can restart `AppDaemon` addon.

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

Thanks to the GitHub Actions, we are able to deploy by just creating a new tag on git. Before proceding with new version bump, make sure to have all the changes for this release in the `RELEASE_NOTES.md` file.

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
