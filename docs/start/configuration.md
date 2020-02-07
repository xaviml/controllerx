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

or:

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: <class of your controller>
  controller: <controller entity id>
  integration: <z2m | deconz | zha>
  media_player: <media player, group entity id>
```

## Real examples

You can check real examples in [here](examples).

## Parameters

These are the generic app parameters for all type of controllers. You can see the rest in [here](type-configuration).

| key             | type           | value                                             | description                                                                                                                                                                                                                                                                            |
| --------------- | -------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`\*      | string         | `controllerx`                                     | The Python module                                                                                                                                                                                                                                                                      |
| `class`\*       | string         | `E1810Controller`                                 | The Python class. Check the classes for each controller on the [supported controllers](/controllerx/controllers) page.                                                                                                                                                                 |
| `controller`\*  | string \| list | `sensor.controller` or `hue_switch1, hue_switch2` | This is the controller id, which will depend on the integration. See [here](/controllerx/how-to/extract-controller-id) to know how to get the controller id.                                                                                                                           |
| `integration`\* | string         | `z2m`, `deconz` or `zha`                          | This is the integration that the device was integrated.                                                                                                                                                                                                                                |
| `actions`       | list           | All actions                                       | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the individual controller pages in [here](/controllerx/controllers).                                                                                                |
| `action_delta`  | int            | 300                                               | This is the threshold time between the previous action and the next one (being the same action). If the time difference between the two actions is less than this attribute, then the action won't be called. I recommend changing this if you see the same action being called twice. |

_\* Required fields_

## What's next?

# [Supported controllers](/controllerx/controllers)
