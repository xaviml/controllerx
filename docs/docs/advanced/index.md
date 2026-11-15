---
title: Custom mapping
description: Replace or extend the default behaviour of a controller with the mapping and merge_mapping parameters.
---

We can use the `mapping` attribute to completely override the default behaviour of a controller, or `merge_mapping` to override just the specified events and keep the rest of the default mapping. Both work the same way:

- **key**: The event fired by the controller. You can check these events in the page of each device in [supported controllers](../controllers/index.md). Note that they change depending on the controller and the integration (z2m, deconz, zha). The [multiple clicks functionality](multiple-clicks.md) can be configured in the `key` part.
- **value**: An [action type](action-types.md) or a list of them. These are the actions executed when the event (`key`) is fired.

Let's see an example:

```yaml
example_app:
  module: controllerx
  class: E1743Controller
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.livingroom
  merge_mapping:
    "off":
      - scene: scene.night
      - service: notify.telegram
        data:
          message: '"off" clicked'
```

In this example, the `key` is `"off"` (extracted from the Zigbee2MQTT mapping of the [E1743 IKEA controller](../controllers/E1743.md#light)) and the value is a list of 2 action types: one to activate a scene and the other to send a message through a HA service call.
