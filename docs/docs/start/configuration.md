---
title: Configuration
description: How to configure ControllerX apps in apps.yaml and the generic parameters available for all controller types.
---

Once [ControllerX has been installed](installation.md), you can proceed to configure ControllerX in `apps.yaml`: `/app_configs/d35634e3_controllerx/apps/apps.yaml` with the ControllerX app, or `apps.yaml` in the AppDaemon apps folder if you installed it manually. This file follows the [AppDaemon specifications](https://appdaemon.readthedocs.io/en/latest/APPGUIDE.html#configuration-of-apps). Each ControllerX app links one controller with one entity (or group of entities), like:

```yaml
example_app:
  module: controllerx
  class: <class of your controller>
  controller: <controller id>
  integration: <z2m | deconz | zha | ...>
  light: <light, group entity id>
```

or:

```yaml
example_app:
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
example_app:
  module: controllerx
  class: <class of your controller>
  controller: <controller entity id>
  integration: <z2m | deconz | zha>
  media_player: <media player, group entity id>
```

or:

```yaml
example_app:
  module: controllerx
  class: <class of your controller>
  controller: <controller entity id>
  integration: <z2m | deconz | zha>
  switch: <switch, group entity id>
```

!!! tip

    The [configuration builder](config-builder.md) generates this configuration for your device.

## Parameters

These are the generic app parameters for all types of controllers. The parameters specific to each controller type (light, media player, switch and cover) are described in [type configuration](type-configuration.md).

| key                    | type           | value                                                                   | description                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------- | -------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`\*             | string         | `controllerx`                                                           | The Python module                                                                                                                                                                                                                                                                                                                                                                                           |
| `class`\*              | string         | `E1810Controller`                                                       | The Python class. Check the classes for each controller on the [supported controllers](../controllers/index.md) page.                                                                                                                                                                                                                                                                                      |
| `controller`\*         | string \| list | `sensor.controller` or `hue_switch1, hue_switch2`                       | The controller ID, which depends on the integration. Each integration page explains how to find it.                                                                                                                                                                                                                                                                   |
| `integration`\*        | string \| dict | See [here](integrations/index.md) the available integrations. | The integration through which the device is connected to Home Assistant.                                                                                                                                                                                                                                                                                                                                                     |
| `actions`              | list           | All actions                                                             | This is a list of actions to be included and controlled by the app. To see the actions of each controller, check its page in [supported controllers](../controllers/index.md). This attribute cannot be used together with `excluded_actions`.                                                                                                                                                     |
| `excluded_actions`     | list           | Empty list                                                              | This is a list of actions to be excluded. To see which actions has each controller check the individual controller pages in [here](../controllers/index.md). This attribute cannot be used together with `actions`.                                                                                                                                                                                        |
| `action_delta`         | dict \| int    | 300                                                                     | This is the threshold time between the previous action and the next one (being the same action). If the time difference between the two actions is less than this attribute, then the action won't be called. I recommend changing this if you see the same action being called twice. A different `action_delta` per action can be defined in a mapping.                                                   |
| `multiple_click_delay` | int            | 500                                                                     | Indicates the delay (in milliseconds) when a multiple click action should be triggered. The higher the number, the more time there can be between clicks, but there will be more delay for the action to be triggered.                                                                                                                                                                                        |
| `action_delay`         | dict \| int    | 0                                                                       | This can be used to set a delay to each action. By default, the delay for all actions is 0. If defining a map, the key for the map is the action and the value is the delay in seconds. Otherwise, we can set a default time like `action_delay: 10`, and this will add a delay to all actions.                                                                                                             |
| `previous_state`       | dict \| str    | -                                                                       | This can be used to restrict when an action is performed depending on the previous state of the entity. This is just applicable for `state` and `z2m` (when not listening to MQTT) integrations. For example, it can be used when we want the action to be triggered only with a specific previous state.                                                                                                                |
| `mapping`              | dict           | -                                                                       | This can be used to replace the behaviour of the controller and manually select what each button should be doing. By default it will ignore this parameter. Read more about it [here](../advanced/index.md). The functionality included in this attribute will remove the default mapping.                                                                                                              |
| `merge_mapping`        | dict           | -                                                                       | This can be used to merge the default mapping from the controller and manually select what each button should be doing. By default it will ignore this parameter. Read more about it in [here](../advanced/index.md). The functionality included in this attribute is added on top of the default mapping.                                                                                                 |
| `mode`                 | dict \| int    | `single`                                                                | This defines what to do when an action is already executing. The options and the behaviour are the same as [Home Assistant automation modes](https://www.home-assistant.io/docs/automation/modes) since it is based on that. The only difference is that `queued` only queues 1 task after the one being executed. One can define a mapping for each action event with different modes. |

Integration dictionary for `integration` attribute.

| key      | type   | value                                                                   | description                                             |
| -------- | ------ | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| `name`\* | string | See [here](integrations/index.md) the available integrations. | This is the integration that the device was integrated. |

In addition, you can add arguments. Each [integration](integrations/index.md) has its own arguments.

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
  # Each integration page explains how to find it: https://xaviml.github.io/controllerx/start/integrations/
  controller: livingroom_controller # or my_controller_id or 00:67:88:56:06:78:9b:3f

  # `integration` is the integration used for your controller
  # It can be a string (e.g. `integration: deconz`) or an object with extra arguments
  # Check https://xaviml.github.io/controllerx/start/integrations/ for more info
  integration:
    name: z2m # or deconz, zha, state, mqtt, etc.
    listen_to: mqtt

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
  # Check https://xaviml.github.io/controllerx/advanced/ for more info
  merge_mapping: # or `mapping`. This is optional.
    brightness_up_click: toggle_full_brightness # use predefined actions
    toggle: # or HA service calls
      service: scene.turn_on
      data:
        entity_id: scene.my_scene
    toggle$2: # These scripts will be called when toggle is fired twice within 500ms (multiple_click_delay)
      - service: script.my_script
      - service: script.my_script_with_arguments
        data:
          my_attr: test

  # From here on, we can include specific attributes from type controllers like
  # Light, MediaPlayer, Switch or Cover controller for example
  # Check https://xaviml.github.io/controllerx/start/type-configuration for more info
  light: light.my_light # or media_player, switch, cover
```
