# z2m_ikea_controller

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

_Bring full functionality to light controllers_

This automation brings the following functionalities lights:

- Turn on/Turn off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.

## Installation

### HACS

The easiest way to add this to your Homeassistant installation is using HACS. And then follow the instructions under Configuration below.

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

And this is a real example for E1524/E1810 controller that controls all the livingroom lights.

```yaml
livingroom_controller:
  module: z2m_ikea_controller
  class: E1810Controller
  sensor: sensor.livingroom_controller_action
  light: group.livingroom_lights
```

You can check in the wiki the [supported controller](https://github.com/xaviml/z2m_ikea_controller/wiki/Supported-controllers).

These are the app parameters:

| key               | optional | type                 | default     | example                                                                                                                                 | description                                                                                                                                                                                                                   |
| ----------------- | -------- | -------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`          | False    | string               | -           | `z2m_ikea_controller`                                                                                                                   | The Python module                                                                                                                                                                                                             |
| `class`           | False    | string               | -           | `E1810Controller`                                                                                                                       | The Python class. Check the classes for each controller on the [supported controllers](https://github.com/xaviml/z2m_ikea_controller/wiki/Supported-controllers) page.                                                        |
| `sensor`          | False    | string \| list       | -           | `sensor.livingroom_controller_action` or `sensor.livingroom_sensor.livingroom_controller_action1, sensor.livingroom_controller_action2` | The sensor(s) entity id from HA. Note that for IKEA E1524/E1810 it finishes with "\_action" by default and for IKEA E1743 with "\_click". This can be also sent as list on the YAML (using "-")                               |
| `light`           | False    | string \| dictionary | -           | `group.livingroom_lights` or `light.kitchen`                                                                                            | The light (or group of lights) you want to control                                                                                                                                                                            |
| `manual_steps`    | True     | int                  | 10          |                                                                                                                                         | Number of steps to go from min to max when clicking. If the value is 2 with one click you will set the light to 50% and with another one to 100%.                                                                             |
| `automatic_steps` | True     | int                  | 10          |                                                                                                                                         | Number of steps to go from min to max when smoothing. If the value is 2 with one click you will set the light to 50% and with another one to 100%.                                                                            |
| `delay`           | True     | int                  | 350         |                                                                                                                                         | Delay in milliseconds that takes between sending the instructions to the light (for the smooth functionality). Note that the maximum value is 1000 and if leaving to 0, you might get uncommon behaviour.                     |
| `actions`         | True     | list                 | All actions |                                                                                                                                         | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the [supported controllers](https://github.com/xaviml/z2m_ikea_controller/wiki/Supported-controllers) page |

Light dictionary for the `light` attribute:

| key          | optional | type   | default | example         | description                                                                                                                                                                                                                                                                                                                                                         |
| ------------ | -------- | ------ | ------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`       | False    | string | -       | `light.kitchen` | The light (or group of lights) you want to control                                                                                                                                                                                                                                                                                                                  |
| `color_mode` | True     | string | `auto`  |                 | This attribute can take `auto`, `xy_color` or `color_temp` as value. `auto` will check first if the light supports `xy_color` and then `color_temp`. `xy_color` will cicle through different colors infinitely. `color_temp` will change the color temperature attribute of the light. If a light supports both, user can pick which action wants for the light(s). |

_TODO_ list:

- [x] Color support
- [ ] Give support to Hue dimmer controller
- [ ] Give support to Symfonisk controller for media_player
- [ ] Change the name of the app by removing _ikea_

_Note: This was tested with Zigbee2MQTT and IKEA devices, but the code does not use any MQTT calls, just Home assistant API._
