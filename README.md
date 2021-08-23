<div align="center">

<h1>ControllerX</h1>

[![logo](https://github.com/xaviml/controllerx/raw/dev/docs/android-chrome-192x192.png)](https://github.com/xaviml/controllerx/releases)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![azure-pipelines-build](https://img.shields.io/azure-devops/build/xaviml93/315b7979-e97e-4004-ac60-8a5cdad5a176/1/main?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=main)
[![last-release](https://img.shields.io/github/v/release/xaviml/controllerx.svg?style=for-the-badge)](https://github.com/xaviml/controllerx/releases)
[![downloads-latest](https://img.shields.io/github/downloads/xaviml/controllerx/latest/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/latest)
[![azure-pipelines-coverage](https://img.shields.io/azure-devops/coverage/xaviml93/315b7979-e97e-4004-ac60-8a5cdad5a176/1/main?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=main)
[![community-topic](https://img.shields.io/badge/community-topic-blue?style=for-the-badge)](https://community.home-assistant.io/t/controllerx-bring-full-functionality-to-light-and-media-player-controllers/148855)
[![buy-me-a-beer](https://img.shields.io/badge/sponsor-Buy%20me%20a%20beer-orange?style=for-the-badge)](https://www.buymeacoffee.com/xaviml)

_Create controller-based automations with ease to control your home devices and scenes._

</div>

## Quick example

With just this configuration, you can have the E1810 controller from IKEA (5 buttons one) connected to the bedroom light and be able to change the brightness and color temperature or color.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
```

## Documentation

You can check the documentation in [here](https://xaviml.github.io/controllerx/).

If you have any question, you can either [open an issue](https://github.com/xaviml/controllerx/issues/new/choose) or comment in [this topic](https://community.home-assistant.io/t/controllerx-bring-full-functionality-to-light-and-media-player-controllers/148855) from the Home Assistant community forum.

If you like this project, don't forget to star it :)

## Contributing

If you want to contribute to this project, check [CONTRIBUTING.md](https://github.com/xaviml/controllerx/blob/main/CONTRIBUTING.md).
