<div align="center">

<h1>ControllerX</h1>

[![logo](https://github.com/xaviml/controllerx/raw/dev/docs/android-chrome-192x192.png)](https://github.com/xaviml/controllerx/releases)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![azure-pipelines-build](https://img.shields.io/azure-devops/build/xaviml93/ControllerX/1/master.svg?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=master)
[![last-release](https://img.shields.io/github/v/release/xaviml/controllerx.svg?style=for-the-badge)](https://github.com/xaviml/controllerx/releases)
[![azure-pipelines-coverage](https://img.shields.io/azure-devops/coverage/xaviml93/ControllerX/1/master.svg?style=for-the-badge)](https://dev.azure.com/xaviml93/ControllerX/_build/latest?definitionId=1&branchName=master)
[![Codacy Badge](https://img.shields.io/codacy/grade/542f29ab55a449099488601ec7400563/master?style=for-the-badge)](https://app.codacy.com/manual/xaviml/controllerx?utm_source=github.com&utm_medium=referral&utm_content=xaviml/controllerx&utm_campaign=Badge_Grade_Dashboard)

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

</div>

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

If you have any question, you can either [open an issue](https://github.com/xaviml/controllerx/issues/new/choose) or comment in [this topic](https://community.home-assistant.io/t/controllerx-bring-full-functionality-to-light-and-media-player-controllers/148855) from the Home Assistant community forum.

If you like this project, don't forget to star it :)

## Contributing

If you want to contribute to this project, check [CONTRIBUTING.md](https://github.com/xaviml/controllerx/blob/master/CONTRIBUTING.md).

_Note: The code does not use any MQTT calls, just the Home Assistant plugin from AppDaemon._
