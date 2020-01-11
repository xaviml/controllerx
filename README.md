# z2m_ikea_controller

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

_Bring full functionality to light and media player controllers_

This automation brings the following functionalities for different [devices](https://github.com/xaviml/z2m_ikea_controller/wiki/Supported-controllers):

- Turn on/Turn off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.
- Play/pause music
- Volume up/down for a media player.

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using HACS with Appdaemon enabled. And then follow the instructions under Configuration below.

### Manual

Download the `z2m_ikea_controller` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `z2m_ikea_controller` module.

## Configuration

This is an example configuration template:

```yaml
nameOfYourInstanceApp:
  module: z2m_ikea_controller
  class: <class of your controller>
  sensor: <sensor(s) entity id>
  light: <light, group entity id>
```

or:

```yaml
nameOfYourInstanceApp:
  module: z2m_ikea_controller
  class: <class of your controller>
  sensor: <sensor(s) entity id>
  light:
    name: <light, group entity id>
    color_mode: auto | xy_color | color_temp
```

This is a real example for E1524/E1810 controller that controls all the livingroom lights.

```yaml
livingroom_controller:
  module: z2m_ikea_controller
  class: E1810Controller
  sensor: sensor.livingroom_controller_action
  light: group.livingroom_lights
```

This is a real example to control a media player with E1744:

```yaml
bedroom_speaker:
  module: z2m_ikea_controller
  class: E1744MediaPlayerController
  sensor: sensor.symfonisk_controller_action
  media_player: media_player.bedroom_speaker
```

These are the generic app parameters for all type of controllers. You can see the rest in [here](https://github.com/xaviml/z2m_ikea_controller/wiki/Controller-types)

| key       | optional | type           | default     | example                                                                                                                                 | description                                                                                                                                                                                                                   |
| --------- | -------- | -------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`  | False    | string         | -           | `z2m_ikea_controller`                                                                                                                   | The Python module                                                                                                                                                                                                             |
| `class`   | False    | string         | -           | `E1810Controller`                                                                                                                       | The Python class. Check the classes for each controller on the [supported controllers](https://github.com/xaviml/z2m_ikea_controller/wiki/Supported-controllers) page.                                                        |
| `sensor`  | False    | string \| list | -           | `sensor.livingroom_controller_action` or `sensor.livingroom_controller_action1, sensor.livingroom_controller_action2` | The sensor(s) entity id from HA. Note that for IKEA E1524/E1810 it finishes with "\_action" by default and for IKEA E1743 with "\_click". This can be also sent as list on the YAML (using "-")                               |
| `actions` | True     | list           | All actions |                                                                                                                                         | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the [supported controllers](https://github.com/xaviml/z2m_ikea_controller/wiki/Supported-controllers) page |

_TODO_ list:

- [x] Color support
- [x] Give support to Hue dimmer controller
- [x] Give support to Symfonisk controller for media_player
- [ ] Change the name of the app by removing _ikea_

_Note: This was tested with Zigbee2MQTT, IKEA devices and the Philips Hue dimmer, but the code does not use any MQTT calls, just the Home Assistant API._
