## Contributing to ControllerX

## Installation

This project uses poetry as python management tool. Run the following commands to install dependencies and hooking up the pre-commit to git

```
poetry install
poetry shell
pre-commit install
```

_Note: I recommend working with Python 3.11, since it is the minimum supported version._

## Adding a new controller

New controllers need to be added to `apps/controllerx/cx_devices/`, and you will need to define the mapping for the integration you are adding support for.

The controller will be added to the documentation automatically, but a JPEG named after the device (e.g. `E1743.jpeg`) needs to be added to `docs/docs/assets/controllers`. If you create a new file in `cx_devices/` for a new manufacturer, add its display name to `MANUFACTURERS` in `docs/main.py`, and if the device needs extra explanations, add them to `docs/notes.yaml`. You can easily find the model (for picture) in the [Zigbee2MQTT supported devices page](https://www.zigbee2mqtt.io/information/supported_devices.html). Check [here](#documentation) to know how to run the documentation locally.

The class name convention should be `Device Model (No special characters) + Type + Controller`. For example, for a new light controller for E1743, the class name should be `E1743LightController`. Take into account that there are some old controllers that do not follow this convention.

Note that this project will only accept the mapping that the original controller would follow with its original hub, or the closest behaviour we can get.

This is a [PR](https://github.com/xaviml/controllerx/pull/482/files) of a complete example of adding a new device, it can be used as a reference.

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

## Committing

You can use the tool `commitizen` to commit based in a standard. If you are in the virtual environment, you can run `cz commit` and answer the questions to commit.

If the commit adds new functionality or fixes something, please add the changes in the `RELEASE_NOTES.md` file.

## Documentation

[Zensical](https://zensical.org) is used for documentation (it reads the existing `docs/mkdocs.yml`). If dependencies are installed with poetry, the following can be executed to get the documentation running locally:

```shell
cd docs
poetry run python gen_device_pages.py
poetry run zensical serve
```

Then, open http://127.0.0.1:8000/controllerx/ in the browser.

The supported controllers pages (`docs/docs/controllers/`) are generated from the code by `gen_device_pages.py` and are not committed: the catalogue (`index.md`), one page per device and `devices.json` (used by the configuration builder and AI tools). Re-run the script after adding or changing a controller to see the changes.

Use relative links to the Markdown files (e.g. `[configuration](../start/configuration.md)`), so the build can check them. `poetry run zensical build --strict` fails on broken links and anchors. The predefined actions documented in `docs/docs/advanced/predefined-actions.md` are checked against the code by `tests/unit_tests/docs_test.py`.

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

Then, make sure to have no other AppDaemon running (like the one you use in Home Assistant), and run:

```shell
docker run --pull=always --rm \
-v $PWD/apps/controllerx:/usr/src/app/conf/apps/controllerx \
-v $PWD/apps.yaml:/usr/src/app/conf/apps/apps.yaml \
-e DASH_URL=http://127.0.0.1:5050 \
-e HA_URL="http://YOUR_HA_IP:8123" \
-e TOKEN="YOUR_HA_TOKEN" \
acockburn/appdaemon:latest
```

This will start AppDaemon with the apps on the `apps.yaml`. Note that if you want to test `mqtt` integration or `z2m` with `listen_to: mqtt`, you will need to execute with MQTT environment variables:

```shell
docker run --pull=always --rm \
-v $PWD/apps/controllerx:/opt/conf/apps/controllerx \
-v $PWD/apps.yaml:/opt/conf/apps/apps.yaml \
-v $PWD/appdaemon.yaml:/opt/conf/appdaemon.yaml.example \
-e DASH_URL=http://127.0.0.1:5050 \
-e HA_URL="http://YOUR_HA_IP:8123" \
-e TOKEN="YOUR_HA_TOKEN" \
-e MQTT_NAMESPACE=mqtt \
-e MQTT_CLIENT_HOST=192.168.X.XXX \
-e MQTT_CLIENT_USER="YOUR_USER" \
-e MQTT_CLIENT_PASSWORD="YOUR_PASSWORD" \
acockburn/appdaemon:latest
```

### Samba app

Install the `Samba share` app in Home Assistant, so you can connect to HA folder structure from your computer. Then, you can copy `apps/controllerx` into the AppDaemon app's apps folder, so that `controllerx.py` ends up in `/app_configs/a0d7b954_appdaemon/apps/controllerx/controllerx.py`. Then, restart the `AppDaemon` app.

Use the AppDaemon app for this, not the ControllerX app: the ControllerX app replaces its `controllerx` folder with the bundled version on every start.

## How to change someone else's PR code

If you have the permission to change code from the source branch of the PR, then you can do the following to change it. Fill in the username and branch and execute the following:

```shell
USERNAME=PR_USER  # Replace
BRANCH=PR_BRANCH  # Replace
git remote add $USERNAME git@github.com:$USERNAME/controllerx.git
git fetch $USERNAME $BRANCH
git checkout -b $USERNAME-$BRANCH $USERNAME/$BRANCH
```

Do your changes and once the changes are committed, you can push with the following command:

```shell
git push $USERNAME HEAD:$BRANCH
```

## Deployment

Thanks to the GitHub Actions, we are able to deploy by just creating a new tag on git. Before proceeding with new version bump, make sure to have all the changes for this release in the `RELEASE_NOTES.md` file.

We use `commitizen` to bump version. Once we are ready to release, we can bump the version and push the tag:

```shell
cz bump
git push origin HEAD --tags
```

_`--dry-run` can be used with `cz` command to double check the version to be created._

When a new tag is created, the CI will automatically generate a GitHub release with the changes for that release, and the release from the `RELEASE_NOTES.md` file.
