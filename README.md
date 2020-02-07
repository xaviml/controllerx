# ControllerX

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![azure-pipelines-build](https://img.shields.io/azure-devops/build/xaviml93/ControllerX/1/dev.svg?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=dev)
[![azure-pipelines-coverage](https://img.shields.io/azure-devops/coverage/xaviml93/ControllerX/1/dev.svg?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=dev)
[![last-release](https://img.shields.io/github/v/release/xaviml/controllerx.svg?style=for-the-badge)](https://github.com/xaviml/controllerx/releases)

## Breaking changes for v2.2.0

:warning: `sensor` and `event_id` are removed from the parameters, now there is a unique parameter called `controller`. So from v2.2.0 you will need to replace `sensor` and `event_id` for `controller`

:warning: You will also need to add a new parameter `integration` to state how the controller is connected with. These are the supported integration, z2m, deconz and zha. This does not mean that there is support for all three integration for all controllers, some controllers do not have some integration due to the lack of the device and being still in development. If you possess a device that is not integrated, you can freely open an issue and I will be glad to help :smiley:

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
