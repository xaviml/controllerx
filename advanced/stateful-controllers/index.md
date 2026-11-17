This page describes how to define a state to execute one action or another depending on the selected state. This is not a ControllerX feature itself, but a combination of the Home Assistant [Input Select](<https://www.home-assistant.io/integrations/input_select/>) (a.k.a. Dropdown) and the AppDaemon [callback constraints](<https://appdaemon.readthedocs.io/en/latest/APPGUIDE.html#callback-constraints>).

In this page, we will go over a simple example to set up a single controller to manage multiple lights. However, this can also be used for other use cases like:

- Change/cycle the state of the controller to run different commands over the same device (e.g. light).
- Cycle through a series of light states.

First, we need to set up an Input Select. Home Assistant allows you to create one through the UI in `Settings > Devices & services > Helpers`, and then clicking `Dropdown`, but we can also create one through YAML:

```
input_select:
  controller_state:
    options:
      - state_0
      - state_1
```

Once we have the entity in Home Assistant, we can create the following ControllerX configurations:

```
example_app_0:
  module: controllerx
  class: E1810Controller
  controller: your_controller
  integration:
    name: z2m
    listen_to: mqtt
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
  controller: your_controller
  integration:
    name: z2m
    listen_to: mqtt
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

From this configuration, we see the following:

- `arrow_left_click` and `arrow_right_click` are used to change the `input_select.controller_state` state. This service cycles through the options, so we could use only one of them (e.g. `input_select.select_next`).
- `constrain_input_select` is used to select which configuration is active depending on the state from `input_select.controller_state`.
- The first configuration controls `light.my_light_1`, and the second one controls `light.my_light_2`.

This particular example could be simplified if we configured the `input_select` with the names of the `light` entities:

```
input_select:
  controller_state:
    options:
      - light.my_light_1
      - light.my_light_2
```

Then, thanks to [templating](<https://xaviml.github.io/controllerx/advanced/templating/index.md>), the configuration would be simplified to the following:

```
example_app:
  module: controllerx
  class: E1810Controller
  controller: your_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: "{{ states('input_select.controller_state') }}"
  merge_mapping:
    arrow_left_click:
      service: input_select.select_previous
      entity_id: input_select.controller_state
    arrow_right_click:
      service: input_select.select_next
      entity_id: input_select.controller_state
```

Note that `constrain_input_select` is no longer necessary, since `light` already has a template that gets the entity name dynamically. However, if we want to do any specific mapping depending on the light, we would need to go back to the previous configuration since it is more flexible and allows us to define a mapping for each state.

The `Advanced` section of the [examples page](<https://xaviml.github.io/controllerx/examples/index.md#advanced>) has more examples using this feature.
