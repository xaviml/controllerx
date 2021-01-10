---
title: Custom mapping
layout: page
---

We can make us of the attribute `mapping` to overwrite completely the behaviour of our default controller, or `merge_mapping` to overwrite just the specified events. The content of both work the same way:
  - **key**: The event to get fired from the controller. You can check these events in the individual pages from the [supported controllers](/controllerx/controllers). Note that they change depending on the controller and the integration (z2m, deconz, zha). [Mutliple click functionality](multiple-clicks) can be configured in the `key` part.
  - **value**: An [action type](action-types) or a list of them. This is/are the action(s) to be executed when the event (`key`) is fired.

Let's see an example:

```yaml
example_app:
  module: controllerx
  class: E1743Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
  merge_mapping:
    "off":
      - scene: scene.night
      - service: notify.telegram
        data:
          message: "off" clicked
```

In this example, the `key` is `"off"` (extracted from the Zigbee2MQTT section of the [E1743 IKEA controller](/controllerx/controllers/E1743#z2m)) and the value is a list of 2 action types: one to activate an scene and the other to send a message through HA call service.
