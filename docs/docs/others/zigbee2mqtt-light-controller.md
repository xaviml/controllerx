---
title: Zigbee2MQTT Light Controller
layout: page
---

_This is supported since ControllerX v4.21.0_

ControllerX has always given support for [Light Controller](/controllerx/start/type-configuration#light-controller) which allows amongst other features to smoothly change attributes (brightness, color temperature) values by requesting the changes periodically to Home Assistant. This has allowed to work with lights integrated with many integrations (e.g.: Zigbee2MQTT, deCONZ, WLED, Hue). However, this generalization has penalized Zigbee2MQTT which has its own mechanism to change brightness and color temp over time which works much smoother than the Light Controller.

Zigbee2MQTT allows to send the following topic `zigbee2mqtt/FRIENDLY_NAME/set` with a payload like `{"brightness_move": -40}` which will change the brightness down with 40 steps over time. Then, we can send to the same topic the following payload to make it stop: `{"brightness_move": "stop"}`. Zigbee2MQTT does not have an specific page with this documentation since it depends on the device itself. For example, we can see all this further explained for the [LED1545G12](https://www.zigbee2mqtt.io/devices/LED1545G12.html#light) light.

ControllerX has always wanted to integrate this inside the Light Controller, but there are many features that are not compatible with what Zigbee2MQTT offers:

- [Hold/Click modes](/controllerx/advanced/hold-click-modes) (bounce, loop)
- Color looping
- Define a minimum and maximum attribute values

For this reason, it has been decided to create a new controller type, [Z2M Light Controller](/controllerx/start/type-configuration#z2m-light-controller), which allows most of the same functionalities as Light Controller, but using MQTT features from Zigbee2MQTT.

Imagine we have a light that in Zigbee2MQTT has friendly name `livingroom` and entity `light.livingroom` in Home Assistant. Then, let's say we had the following ControllerX configuration for [E1810](/controllerx/controllers/E1810):

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller # (1)
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
```

1. `E1810Controller` is a `Light Controller`

This allows us to control the the `livingroom` light with the Light Controller, however if we replace `E1810Controller` for the new `E1810Z2MLightController` and the `light.livingroom` for `livingroom` we will be using Z2M Light Controller:

```yaml hl_lines="3 6"
livingroom_controller:
  module: controllerx
  class: E1810Z2MLightController # (1)
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: livingroom # (2)
```

1.  This is a `Z2M Light Controller`
2.  This the Zigbee2MQTT friendly name

This will be sending MQTT messages through Home Assistant, but if we have the [MQTT plugin enabled](/controllerx/others/enable-mqtt-plugin) in AppDaemon, then we could send the MQTT through MQTT plugin:

```yaml hl_lines="6 7 8"
livingroom_controller:
  module: controllerx
  class: E1810Z2MLightController
  controller: sensor.livingroom_controller_action
  integration: z2m
  light:
    name: livingroom
    mode: mqtt # (1)
```

1.  `mode` can either be `ha` or `mqtt` (default: `ha`). On the one hand, `ha` will send the mqtt messages through Home Assistant with [`mqtt.publish` service](https://www.home-assistant.io/docs/mqtt/service/#service-mqttpublish). On the other hand, `mqtt` will send the MQTT messages through MQTT plugin from AppDaemon (hence skipping HA).

Finally, we can have the full ControllerX configuration listening and sending to MQTT broker directly without going through Home Assistant:

```yaml hl_lines="5 6 7"
livingroom_controller:
  module: controllerx
  class: E1810Z2MLightController
  controller: livingroom_controller # (1)
  integration:
    name: z2m
    listen_to: mqtt
  light:
    name: livingroom
    mode: mqtt
```

1.  `livingroom_controller` is the Zigbee2MQTT friendly name of the controller

With this latest configuration, we can keep using the light even if Home Assistant is down since all interactions go:

```
Zigbee2MQTT <> MQTT Broker <> AppDaemon (ControllerX)
```

Many of the existing devices now have support to `Z2MLightController`, and you can use it in the `class` as you can now use `LightController` as well. Check [Supported controllers](/controllerx/controllers) pages to see the class names.
