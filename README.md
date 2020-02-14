# ControllerX

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![azure-pipelines-build](https://img.shields.io/azure-devops/build/xaviml93/ControllerX/1/master.svg?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=master)
[![azure-pipelines-coverage](https://img.shields.io/azure-devops/coverage/xaviml93/ControllerX/1/master.svg?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=master)
[![last-release](https://img.shields.io/github/v/release/xaviml/controllerx.svg?style=for-the-badge)](https://github.com/xaviml/controllerx/releases)

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

## Quick example

With just this configuration, you can have the E1810 controller from IKEA (5 buttons one) connected to the bedroom light and be able to change the brightness and color temperature or color.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.bedroom
```

## Documentation

You can check the documentation in [here](https://xaviml.github.io/controllerx/).

## Contributing

If you want to contribute to this project, check [CONTRIBUTING.md](/CONTRIBUTING.md).

_Note: The code does not use any MQTT calls, just the Home Assistant plugin from AppDaemon._
