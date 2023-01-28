---
title: Stateful Controllers
layout: page
---

This page describes how to define an state to execute one action or another depending on the state selected. This is a feature that is not necessarily from ControlleX, but from to [Input Select](https://www.home-assistant.io/integrations/input_select/) (a.k.a. Dropdown) from Home Assistant, and [Callback Constraints](https://appdaemon.readthedocs.io/en/latest/APPGUIDE.html#callback-constraints) from AppDaemon.

Through this page we will go over an easy example to setup a single controller to manage multiple lights. However, this can also be used for other use cases like:

- Change/cycle the state of the controller to run different commands over the same device (e.g. light).
- Cycle through a series of light states.

First, we will need to setup an Input Select. Home Assistant allows you to create one through UI on `Settings -> Devices & Services -> Helpers`, and then clicking `Dropdown`, but we can also create one through YAML:

```yaml
input_select:
  controller_state:
    options:
      - state_0
      - state_1
```

Once we have an entity that Home Assistant controls, we can create the following ControllerX configs:

```yaml
example_app_0:
  module: controllerx
  class: E1810Controller
  controller: sensor.your_controller_action
  integration: z2m
  light: light.my_light_1
  merge_mapping:
    arrow_left_click:
      service: input_select.select_previous
      entity_id: input_select.controller_state
    arrow_right_click:
      service: input_select.select_next
      entity_id: input_select.controller_state
  constrain_input_select: input_select.controller_state,state_0

example_app_1:
  module: controllerx
  class: E1810Controller
  controller: sensor.your_controller_action
  integration: z2m
  light: light.my_light_2
  merge_mapping:
    arrow_left_click:
      service: input_select.select_previous
      entity_id: input_select.controller_state
    arrow_right_click:
      service: input_select.select_next
      entity_id: input_select.controller_state
  constrain_input_select: input_select.controller_state,state_1
```

From these configuration we see the following:

- `arrow_left_click` and `arrow_right_click` are used to change the `input_select.controller_state` state. This service will cycle through the options, so we could have only one (e.g. `input_select.select_next`).
- `constrain_input_select` is used to select which configuration is active depending on the state from `input_select.controller_state`.
- First config controls `light.my_light_1`, and the second one controls `light.my_light_2`.

This particular example, could be simplified if we configured the `input_select` with the `light` entities names:

```yaml
input_select:
  controller_state:
    options:
      - light.my_light_1
      - light.my_light_2
```

Then, the configuration would be simplified to the following thanks to [templating](./templating.md):

{% set special = "{{ states('input_select.controller_state') }}" %}

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: sensor.your_controller_action
  integration: z2m
  light: "{{ special }}"
  merge_mapping:
    arrow_left_click:
      service: input_select.select_previous
      entity_id: input_select.controller_state
    arrow_right_click:
      service: input_select.select_next
      entity_id: input_select.controller_state
```

Note that the `constrain_input_select` is no longer necessary since the `light` already has a template that checks the name dynamically. However, if we want to do any specific mapping depending on the light, we would need to go back to the previous configuration since it is more flexible and allows us to define a mapping for each state.

In the `Advanced` section from the [examples page](../examples/index.md#advanced), we can see some examples using this feature.
