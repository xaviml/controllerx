---
layout: page
title: Configuration
---

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


## What's next?

# [Supported controllers](/controllers)