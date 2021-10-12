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

| key                    | type           | value                                             | description                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------- | -------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`\*             | string         | `controllerx`                                     | The Python module                                                                                                                                                                                                                                                                                                                                                                                           |
| `class`\*              | string         | `E1810Controller`                                 | The Python class. Check the classes for each controller on the [supported controllers](/controllerx/controllers) page.                                                                                                                                                                                                                                                                                      |
| `controller`\*         | string \| list | `sensor.controller` or `hue_switch1, hue_switch2` | This is the controller id, which will depend on the integration. See [here](/controllerx/others/extract-controller-id) to know how to get the controller id.                                                                                                                                                                                                                                                |
| `integration`\*        | string \| dict | `z2m`, `deconz` or `zha`                          | This is the integration that the device was integrated.                                                                                                                                                                                                                                                                                                                                                     |
| `actions`              | list           | All actions                                       | This is a list of actions to be included and controlled by the app. To see which actions has each controller check the individual controller pages in [here](/controllerx/controllers). This attribute cannot be used together with `excluded_actions`.                                                                                                                                                     |
| `excluded_actions`     | list           | Empty list                                        | This is a list of actions to be excluded. To see which actions has each controller check the individual controller pages in [here](/controllerx/controllers). This attribute cannot be used together with `actions`.                                                                                                                                                                                        |
| `action_delta`         | dict \| int    | 300                                               | This is the threshold time between the previous action and the next one (being the same action). If the time difference between the two actions is less than this attribute, then the action won't be called. I recommend changing this if you see the same action being called twice. A different `action_delta` per action can be defined in a mapping.                                                   |
| `multiple_click_delay` | int            | 500                                               | Indicates the delay (in milliseconds) when a multiple click action should be trigger. The higher the number, the more time there can be between clicks, but there will be more delay for the action to be triggered.                                                                                                                                                                                        |
| `action_delay`         | dict \| int    | 0                                                 | This can be used to set a delay to each action. By default, the delay for all actions is 0. If defining a map, the key for the map is the action and the value is the delay in seconds. Otherwise, we can set a default time like `action_delay: 10`, and this will add a delay to all actions.                                                                                                             |
| `mapping`              | dict           | -                                                 | This can be used to replace the behaviour of the controller and manually select what each button should be doing. By default it will ignore this parameter. Read more about it in [here](/controllerx/advanced/custom-controllers). The functionality included in this attribute will remove the default mapping.                                                                                           |
| `merge_mapping`        | dict           | -                                                 | This can be used to merge the default mapping from the controller and manually select what each button should be doing. By default it will ignore this parameter. Read more about it in [here](/controllerx/advanced/custom-controllers). The functionality included in this attribute is added on top of the default mapping.                                                                              |
| `mode`                 | dict \| int    | `single`                                          | This has the purpose of defining what to do when an ation(s) is/are executing. The options and the behaviour is the same as [Home Assistant automation modes](https://www.home-assistant.io/docs/automation/modes) since it is based on that. The only difference is that `queued` only queues 1 task after the one is being executed. One can define a mapping for each action event with different modes. |

Integration dictionary for `integration` attribute.

| key      | type   | value                    | description                                             |
| -------- | ------ | ------------------------ | ------------------------------------------------------- |
| `name`\* | string | `z2m`, `deconz` or `zha` | This is the integration that the device was integrated. |

In addition, you can add arguments. Each [integration](/controllerx/others/integrations) has its own arguments.

_\* Required fields_

#### Explained with YAML

```yaml
example_app: # It can be anything
  module: controllerx

  # `class` value depends on the controller you want to use
  # Check the classes for each controller on the supported controllers page
  # Supported controller page: https://xaviml.github.io/controllerx/controllers/
  class: Controller # or E1810Controller, LightController, HueDimmerController, etc.

  # `controller` value depends on the integration used (z2m, deconz, zha).
  # Check https://xaviml.github.io/controllerx/others/extract-controller-id for more info
  controller: sensor.my_controller_action # or my_controller_id or 00:67:88:56:06:78:9b:3f

  # `integration` is the integration used for your controller
  # It can be used as object like:
  # integration:
  #   name: z2m
  #   listen_to: mqtt
  # Check https://xaviml.github.io/controllerx/others/integrations for more info
  integration: z2m # or deconz, mqtt, zha, state

  # `actions` and `excluded_actions` can be used to indicate which actions from the default mapping
  # will be used or not. These 2 attributes cannot be used at the same time.
  actions: # or excluded_actions. This is optional.
    - toggle
    - brightness_up_click

  # `action_delta` is the threshold to avoid firing the same action twice
  action_delta: 300 # default. This is optional.

  # `multiple_click_delay` is used for the multiclick functionality
  # Check https://xaviml.github.io/controllerx/advanced/multiple-clicks for more info
  multiple_click_delay: 500 # default. This is optional.

  # `action_delay` lets you configure delays to existing actions
  action_delay: # This is optional.
    toggle: 10 # This will fire `toggle` action in 10 seconds after pressed.

  # `mode` allows you to define the strategy when an action is already executing
  # Possible values are `single`, `restart`, `queued` and `parallel`
  mode: single # default. This is optional.

  # `mapping` and `merge_mapping` let you override the default behaviour of your controller.
  # `merge_mapping` updates the default mapping, and `mapping` overrides it completely.
  # Check https://xaviml.github.io/controllerx/advanced/custom-controllers for more info
  merge_mapping: # or `mapping`. This is optional.
    brightness_up_click: toggle_full_brightness # use predefined actions
    toggle: # or HA service calls
      service: scene.turn_on
      data:
        entity_id: scene.my_scene
    toggle$2: # This scripts will be called when toggle is fired twice within 500ms (multiple_click_delay)
      - service: script.my_script
      - service: script.my_script_with_arguments
        data:
          my_attr: test

  # From here on, we can include specific attribute from type controllers like
  # Light, MediaPlayer, Switch or Cover controller for example
  # Check https://xaviml.github.io/controllerx/start/type-configuration for more info
  light: light.my_light # or media_player, switch, cover
```

## What's next?

# [Supported controllers](/controllerx/controllers)
