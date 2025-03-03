---
title: Event integration
layout: page
---

_This is supported since ControllerX v4.23.0_

Most of the integrations supported by ControllerX are defined for an specific use case (zigbee2mqtt, deCONZ, ZHA), but we also have the [`State` integration](/controllerx/start/integrations/state), which is a more generic integration and allows us to listen to any Home Assistant entity state and build a mapping from it. From ControllerX v4.23.0, we can also use the [`Event` integration](/controllerx/start/integrations/event) which allows us define the event we want to listen to, and which actions build from it.

Each event has its own payload that could look like:

```json
{
  "device_ieee": "00:67:88:56:06:78:9b:3f",
  "device_name": "my_device",
  "command": "step",
  "args": { "direction": "up" }
}
```

Then, ControllerX needs to convert this JSON-like data to an action string, so we can build our mapping on something like `action_step_up`.

Following this use case, we can create our own ControllerX configuration with this custom event:

```yaml
example_app:
  module: controllerx
  class: LightController
  controller: my_device # This is the value we listen from `controller_key` defined below.
  light: light.my_light
  integration:
    name: event # This name is necessary
    event_type: my_custom_event
    controller_key: device_name
    action_template: "action_{command}_{args[direction]}"
  mapping:
    action_step_up: click_brightness_up
    action_step_down: click_brightness_down
```

Let's break down the configuration for the integration:

- `event_type`: This is the event we will be listening to. For example, ZHA uses `zha_event`.
- `controller_key`: This is the key that we will listen from. It can be extracted from the event. Note that the following names cannot be used for this field: `name`, `event`, `callback`, `namespace` or `cb`
- `action_template`: This is the template that allows us build the name of the actions. We can use `{}` to retrieve the keys from the data, and `[]` inside to access attributes inside it as shown in the example.
