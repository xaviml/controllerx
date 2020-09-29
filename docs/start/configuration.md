---
layout: page
title: Configuration
---

This is an example configuration template to place in `/config/appdaemon/apps/apps.yaml`:

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

or:

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: <class of your controller>
  controller: <controller entity id>
  integration: <z2m | deconz | zha>
  switch: <switch, group entity id>
```

## Real examples

You can check real examples in [here](/controllerx/examples).

#### 💡 **NOTE**

When using words like "on" and "off" in the YAML configuration,
you will need to wrap them up with quotation marks ("),
otherwise they will be parsed as boolean variables (True and False).

## Parameters

These are the generic app parameters for all type of controllers. You can see the rest in [here](type-configuration).

| key                    | type           | value                                             | description                                                                                                                                                                                                                                                                            |
| ---------------------- | -------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`\*             | string         | `controllerx`                                     | The Python module                                                                                                                                                                                                                                                                      |
| `class`\*              | string         | `E1810Controller`                                 | The Python class. Check the classes for each controller on the [supported controllers](/controllerx/controllers) page.                                                                                                                                                                 |
| `controller`\*         | string \| list | `sensor.controller` or `hue_switch1, hue_switch2` | This is the controller id, which will depend on the integration. See [here](/controllerx/others/extract-controller-id) to know how to get the controller id.                                                                                                                           |
| `integration`\*        | string \| dict | `z2m`, `deconz` or `zha`                          | This is the integration that the device was integrated.                                                                                                                                                                                                                                |
| `actions`              | list           | All actions                                       | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the individual controller pages in [here](/controllerx/controllers). This attribute cannot be used together with `excluded_actions`.                                |
| `excluded_actions`     | list           | Empty list                                        | This is a list of actions to be excluded. To see which actions has each controller check the individual controller pages in [here](/controllerx/controllers). This attribute cannot be used together with `actions`.                                                                   |
| `action_delta`         | int            | 300                                               | This is the threshold time between the previous action and the next one (being the same action). If the time difference between the two actions is less than this attribute, then the action won't be called. I recommend changing this if you see the same action being called twice. |
| `multiple_click_delay` | int            | 1000                                              | Indicates the delay (in milliseconds) when a multiple click action should be trigger. The higher the number, the more time there can be between clicks, but there will be more delay for the action to be triggered.                                                                   |
| `action_delay`         | dict           | -                                                 | This can be used to set a delay to each action. By default, the delay for all actions is 0. The key for the map is the action and the value is the delay in seconds.                                                                                                                   |
| `mapping`              | dict           | -                                                 | This can be used to replace the behaviour of the controller and manually select what each button should be doing. By default it will ignore this parameter. Read more about it in [here](/controllerx/others/custom-controllers).                                                      |

Integration dictionary for `integration` attribute.

| key      | type   | value                    | description                                             |
| -------- | ------ | ------------------------ | ------------------------------------------------------- |
| `name`\* | string | `z2m`, `deconz` or `zha` | This is the integration that the device was integrated. |

In addition, you can add arguments. Each [integration](/controllerx/others/integrations) has its own arguments.

_\* Required fields_

## What's next?

# [Supported controllers](/controllerx/controllers)
