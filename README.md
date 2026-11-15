<div align="center">

<h1>ControllerX</h1>

<img src="https://github.com/xaviml/controllerx/blob/main/docs/docs/assets/logo_blue.png" width="192" height="192"/>

[![github-check-status](https://img.shields.io/github/checks-status/xaviml/controllerx/main?style=for-the-badge)](https://github.com/xaviml/controllerx/actions?query=branch%3Amain)
[![last-release](https://img.shields.io/github/v/release/xaviml/controllerx.svg?style=for-the-badge)](https://github.com/xaviml/controllerx/releases)
[![downloads-latest](https://img.shields.io/github/downloads/xaviml/controllerx/latest/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/latest)
[![code-coverage](https://img.shields.io/codecov/c/gh/xaviml/controllerx/main?style=for-the-badge&token=7PUZHL97IG)](https://app.codecov.io/gh/xaviml/controllerx/branch/main)
[![community-topic](https://img.shields.io/badge/community-topic-blue?style=for-the-badge)](https://community.home-assistant.io/t/controllerx-bring-full-functionality-to-light-and-media-player-controllers/148855)
[![buy-me-a-beer](https://img.shields.io/badge/sponsor-Buy%20me%20a%20beer-orange?style=for-the-badge)](https://www.buymeacoffee.com/xaviml)

_Create controller-based automations with ease to control your home devices and scenes._

</div>

## Quick example

With just this configuration, you can have the E2002 controller from IKEA (4 buttons) connected to the livingroom light and be able to change the brightness and color temperature or color.

```yaml
livingroom_controller:
  module: controllerx
  class: E2002LightController
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.livingroom
```

## Installation

Install ControllerX as a Home Assistant app (recommended), or manually in the AppDaemon app. See the [installation guide](https://xaviml.github.io/controllerx/start/installation).

[![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fxaviml%2Fcontrollerx-app)

## Documentation

You can check the documentation in [here](https://xaviml.github.io/controllerx/).

[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

If you have any question, you can either [open an issue](https://github.com/xaviml/controllerx/issues/new/choose) or comment in [this topic](https://community.home-assistant.io/t/controllerx-bring-full-functionality-to-light-and-media-player-controllers/148855) from the Home Assistant community forum.

If you like this project, don't forget to star it :)

## Contributing

If you want to contribute to this project, check [CONTRIBUTING.md](https://github.com/xaviml/controllerx/blob/main/CONTRIBUTING.md).
