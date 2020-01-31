# ControllerX

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

## Breaking changes

:warning: This app has lost the support for AppDaemon 3.x, please migrate to AppDaemon 4.x. The hassio addon for it has been released recently.

:warning: The module is called now controllerx.

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

This automation brings the following functionalities for different [devices](https://github.com/xaviml/controllerx/wiki/Supported-controllers):

- Turn on/Turn off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.
- Play/pause music
- Volume up/down for a media player.

The appdaemon app supports zigbee2mqtt (use the `sensor` parameter) and deConz (use the `event_id` parameter).

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using HACS with Appdaemon enabled. And then follow the instructions under Configuration below.

### Manual

Download the `controllerx` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `controllerx` module.

## Configuration

This is an example configuration template:

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: <class of your controller>
  sensor: <sensor(s) entity id>
  light: <light, group entity id>
```

or:

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: <class of your controller>
  sensor: <sensor(s) entity id>
  light:
    name: <light, group entity id>
    color_mode: auto | xy_color | color_temp
```

This is a real example for E1524/E1810 controller that controls all the livingroom lights.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  sensor: sensor.livingroom_controller_action
  light: group.livingroom_lights
```

This is a real example to control a media player with E1744:

```yaml
bedroom_speaker:
  module: controllerx
  class: E1744MediaPlayerController
  sensor: sensor.symfonisk_controller_action
  media_player: media_player.bedroom_speaker
```

These are the generic app parameters for all type of controllers. You can see the rest in [here](https://github.com/xaviml/controllerx/wiki/Controller-types)

| key            | optional | type           | default        | example                                                         | description                                                                                                                                                                                                                                                                                                            |
| -------------- | -------- | -------------- | -------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`       | False    | string         | -              | `controllerx`                                                   | The Python module                                                                                                                                                                                                                                                                                                      |
| `class`        | False    | string         | -              | `E1810Controller`                                               | The Python class. Check the classes for each controller on the [supported controllers](https://github.com/xaviml/controllerx/wiki/Supported-controllers) page.                                                                                                                                                         |
| `sensor`       | False    | string \| list | -              | `sensor.controller` or `sensor.controller1, sensor.controller2` | The sensor(s) entity id from HA. Note that for IKEA E1524/E1810 it finishes with "\_action" by default and for IKEA E1743 with "\_click". `sensor` and `event_id` cannot be used together. This attribute could be used for devices integrated with zigbee2mqtt. This can be also sent as list on the YAML (using "-") |
| `event_id`     | False    | string \| list | -              | `hue_switch` or `hue_switch1, hue_switch2`                      | The event id(s). `sensor` and `event_id` cannot be used together. This attribute could be used for devices integrated with deConz. This can be also sent as list on the YAML (using "-")                                                                                                                               |
| `event`        | True     | string         | `deconz_event` |                                                                 | The event feature was meant to be used for devices integrated with deConz, but the event can be overwritten for other use cases.                                                                                                                                                                                       |
| `actions`      | True     | list           | All actions    |                                                                 | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the [supported controllers](https://github.com/xaviml/controllerx/wiki/Supported-controllers) page                                                                                                  |
| `action_delta` | True     | int            | 300            |                                                                 | This is the threshold time between the previous action and the next one (being the same action). If the time difference between the two actions is less than this attribute, then the action won't be called. I recommend changing this if you see the same action being called twice.                                 |

## Contributing

See [CONTRIBUTING.md](/CONTRIBUTING.md)

_Note: The code does not use any MQTT calls, just the Home Assistant API from AppDaemon._
