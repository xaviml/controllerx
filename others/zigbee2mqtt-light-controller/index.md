*This is supported since ControllerX v4.21.0*

ControllerX has always supported the [Light Controller](<https://xaviml.github.io/controllerx/start/type-configuration/index.md#light-controller>), which, amongst other features, smoothly changes attributes (brightness, color temperature) by periodically requesting the changes to Home Assistant. This works with lights from many integrations (e.g. Zigbee2MQTT, deCONZ, WLED, Hue). However, this generalization penalizes Zigbee2MQTT, which has its own mechanism to change the brightness and color temperature over time, and works much more smoothly than the Light Controller.

Zigbee2MQTT allows sending a payload like `{"brightness_move": -40}` to the `zigbee2mqtt/FRIENDLY_NAME/set` topic, which decreases the brightness 40 steps per second over time. Then, we can send the following payload to the same topic to make it stop: `{"brightness_move": "stop"}`. Zigbee2MQTT does not have a specific page documenting this, since it depends on the device. For example, we can see all this further explained for the [LED1545G12](<https://www.zigbee2mqtt.io/devices/LED1545G12.html#light>) light.

Ideally, this would be part of the Light Controller, but there are many features that are not compatible with what Zigbee2MQTT offers:

- [Hold/Click modes](<https://xaviml.github.io/controllerx/advanced/hold-click-modes/index.md>) (bounce, loop)
- Color looping
- Minimum and maximum attribute values

For this reason, there is a separate controller type, [Z2M Light Controller](<https://xaviml.github.io/controllerx/start/type-configuration/index.md#zigbee2mqtt-light-controller>), which offers most of the functionality of the Light Controller, but uses the MQTT features from Zigbee2MQTT.

Imagine we have a light with the friendly name `livingroom` in Zigbee2MQTT and the entity `light.livingroom` in Home Assistant. Then, let's say we had the following ControllerX configuration for [E1810](<https://xaviml.github.io/controllerx/controllers/E1810/index.md>):

```
livingroom_controller:
  module: controllerx
  class: E1810Controller # (1)
  controller: livingroom_controller_action
  integration:
    name: z2m
    listen_to: event
  light: light.livingroom
```

1. `E1810Controller` is a `Light Controller`

This allows us to control the `livingroom` light with the Light Controller. However, if we replace `E1810Controller` with `E1810Z2MLightController`, and `light.livingroom` with `livingroom`, we will be using the Z2M Light Controller:

```
livingroom_controller:
  module: controllerx
  class: E1810Z2MLightController # (1)
  controller: livingroom_controller_action
  integration:
    name: z2m
    listen_to: event
  light: livingroom # (2)
```

1. This is a `Z2M Light Controller`
2. This is the Zigbee2MQTT friendly name of the light

This sends the MQTT messages through Home Assistant, but if we have the [MQTT plugin enabled](<https://xaviml.github.io/controllerx/others/enable-mqtt-plugin/index.md>) in AppDaemon, we can send them through the MQTT plugin instead:

```
livingroom_controller:
  module: controllerx
  class: E1810Z2MLightController
  controller: livingroom_controller_action
  integration:
    name: z2m
    listen_to: event
  light:
    name: livingroom
    mode: mqtt # (1)
```

1. `mode` can either be `ha` or `mqtt` (default: `ha`). On the one hand, `ha` sends the MQTT messages through Home Assistant with the [`mqtt.publish` service](<https://www.home-assistant.io/docs/mqtt/service/#service-mqttpublish>). On the other hand, `mqtt` sends the MQTT messages through the AppDaemon MQTT plugin (hence skipping HA).

Finally, we can have ControllerX both listening and sending to the MQTT broker directly, without going through Home Assistant:

```
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

1. `livingroom_controller` is the Zigbee2MQTT friendly name of the controller

With this configuration, we can keep using the light even if Home Assistant is down, since all the interactions go:

```
Zigbee2MQTT <> MQTT Broker <> AppDaemon (ControllerX)
```

Many of the supported devices have a Zigbee2MQTT light controller class, which can be used in `class` the same way as their light controller class. Check the [supported controllers](<https://xaviml.github.io/controllerx/controllers/index.md>) pages to see the class names.
