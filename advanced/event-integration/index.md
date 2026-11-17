*This is supported since ControllerX v4.23.0*

Most of the integrations supported by ControllerX are defined for a specific use case (Zigbee2MQTT, deCONZ, ZHA), but there is also the [`State` integration](<https://xaviml.github.io/controllerx/start/integrations/state/index.md>), a more generic integration that allows us to listen to any Home Assistant entity state and build a mapping from it. Since ControllerX v4.23.0, we can also use the [`Event` integration](<https://xaviml.github.io/controllerx/start/integrations/event/index.md>), which allows us to define the event we want to listen to and how to build the actions from it.

Each event has its own payload that could look like:

```
{
  "device_ieee": "00:67:88:56:06:78:9b:3f",
  "device_name": "my_device",
  "command": "step",
  "args": { "direction": "up" }
}
```

Then, ControllerX needs to convert this JSON-like data into an action string, such as `action_step_up`, so we can build our mapping on it.

Following this use case, we can create our own ControllerX configuration with this custom event:

```
example_app:
  module: controllerx
  class: LightController
  controller: my_device # The value of the `controller_key` attribute defined below
  light: light.my_light
  integration:
    name: event # Required
    event_type: my_custom_event
    controller_key: device_name
    action_template: "action_{command}_{args[direction]}"
  mapping:
    action_step_up: click_brightness_up
    action_step_down: click_brightness_down
```

Let's break down the configuration for the integration:

- `event_type`: This is the event we will be listening to. For example, ZHA uses `zha_event`.
- `controller_key`: This is the attribute of the event data that identifies the controller. Its value must match the `controller` parameter. Note that the following names cannot be used for this field: `name`, `event`, `callback`, `namespace` or `cb`.
- `action_template`: This is the template used to build the name of the actions. We can use `{}` to retrieve the keys from the data, and `[]` inside them to access nested attributes, as shown in the example.
