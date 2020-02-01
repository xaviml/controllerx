# ControllerX

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

## Breaking changes

:warning: `sensor` and `event_id` are removed from the parameters, now there is a unique parameter called `controller`. So from v2.2.0 you will need to replace `sensor` and `event_id` for `controller`

:warning: You will also need to add a new parameter `integration` to state how the controller is connected with. These are the supported integration, z2m, deconz and zha. This does not mean that there is support for all three integration for all controllers, some controllers do not have some integration due to the lack of the device and being still in development. If you possess a device that is not integrated, you can freely open an issue and I will be glad to help :smiley:

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

This automation brings the following functionalities for different [devices](https://github.com/xaviml/controllerx/wiki/Supported-controllers):

- Turn on/Turn off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.
- Play/pause music
- Volume up/down for a media player.

This project gives support now to controllers integrated with zigbee2mqtt, deCONZ and ZHA.

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using HACS with Appdaemon enabled. And then follow the instructions under Configuration below.

### Manual

Download the `controllerx` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `controllerx` module.

## Update
Note that AppDaemon will need to be restarted when installing a new version of ControllerX. This is due to AppDaemon not reimporting the modules again. If AppDaemon server is not restarted, then it will keep executing the old version.

## Configuration

This is an example configuration template:

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: <class of your controller>
  controller: <controller entity id>
  integration: <z2m | deconz | zha>
  light: <light, group entity id>
```

or:

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: <class of your controller>
  controller: <controller entity id>
  integration: <z2m | deconz | zha>
  light:
    name: <light, group entity id>
    color_mode: auto | xy_color | color_temp
```

This is a real example for E1524/E1810 controller with z2m that controls all the livingroom lights.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: group.livingroom_lights
```

This is a real example to control a media player with E1744 with deCONZ:

```yaml
bedroom_speaker:
  module: controllerx
  class: E1744MediaPlayerController
  controller: symfonisk_controller
  integration: deconz
  media_player: media_player.bedroom_speaker
```

These are the generic app parameters for all type of controllers. You can see the rest in [here](https://github.com/xaviml/controllerx/wiki/Controller-types)

| key            | optional | type           | default     | example                                           | description                                                                                                                                                                                                                                                                            |
| -------------- | -------- | -------------- | ----------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`       | False    | string         | -           | `controllerx`                                     | The Python module                                                                                                                                                                                                                                                                      |
| `class`        | False    | string         | -           | `E1810Controller`                                 | The Python class. Check the classes for each controller on the [supported controllers](https://github.com/xaviml/controllerx/wiki/Supported-controllers) page.                                                                                                                         |
| `controller`   | False    | string \| list | -           | `sensor.controller` or `hue_switch1, hue_switch2` | This is the controller id. This will change depending on the integration. In case of `z2m` is the name of the sensor in HA, it normally finishes with `_action`. For `deconz` is the device name given on the phoscon app. And finally, for `zha` is the device IEEE.                  |
| `integration`  | False    | string         | -           | `z2m`, `deconz` or `zha`                          | This is the integration that the device was integrated.                                                                                                                                                                                                                                |
| `actions`      | True     | list           | All actions |                                                   | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the [supported controllers](https://github.com/xaviml/controllerx/wiki/Supported-controllers) page                                                                  |
| `action_delta` | True     | int            | 300         |                                                   | This is the threshold time between the previous action and the next one (being the same action). If the time difference between the two actions is less than this attribute, then the action won't be called. I recommend changing this if you see the same action being called twice. |

## Contributing

See [CONTRIBUTING.md](/CONTRIBUTING.md)

_Note: The code does not use any MQTT calls, just the Home Assistant API from AppDaemon._
