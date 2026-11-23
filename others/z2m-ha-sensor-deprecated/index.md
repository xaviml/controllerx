*Zigbee2MQTT HA sensor deprecated since ControllerX v4.29.0*

Zigbee2MQTT 2.0.0 brought [some breaking changes](<https://github.com/Koenkk/zigbee2mqtt/discussions/24198>), and one of them was to deprecate the [Home Assistant action sensors](<https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html#via-home-assistant-action-sensor-deprecated>), which is the default option of the [Zigbee2MQTT integration](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) in ControllerX.

You might be here because of a warning in the AppDaemon logs that looks like the following:

> [!NOTE]
>
> **Quote**
>
> ⚠️ Listening to HA sensor actions is now deprecated and will be removed in the future. Use `listen_to: mqtt` or `listen_to: event` instead. Read more about it here: https://xaviml.github.io/controllerx/others/z2m-ha-sensor-deprecated

This might be because your controller configuration looks like:

```
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
```

The issue is `integration: z2m`, which reads a HA `sensor` by default. You need to switch to either [`mqtt`](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md#mqtt-topics-listen_to-mqtt>) (recommended) or HA [`event`](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md#event-state-listen_to-event>) (experimental).

## Switch to MQTT listener (recommended)

To switch to MQTT (as [recommended by Zigbee2MQTT](<https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html#via-mqtt-device-trigger-recommended>)), you first need to [enable the MQTT plugin](<https://xaviml.github.io/controllerx/others/enable-mqtt-plugin/index.md>). Then, change your configuration to something like the following:

```
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller # (1)
  integration:
    name: z2m
    listen_to: mqtt # (2)
  light: light.livingroom
```

1. This is the friendly name of the device in Zigbee2MQTT. Check [here](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md#mqtt-topics-listen_to-mqtt>) how to get this value.
2. With `mqtt`, ControllerX listens to the MQTT topic of the controller.

## Switch to HA Event sensor listener (experimental)

Another option is to listen to the new (and experimental) event entity from Zigbee2MQTT 2.0.0. First, enable the experimental feature in Zigbee2MQTT as explained [here](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md#event-state-listen_to-event>). Then, change your configuration to something like:

```
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller_action # (1)
  integration:
    name: z2m
    listen_to: event # (2)
  light: light.livingroom
```

1. This is the event entity without the `event.` prefix. Check [here](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md#event-state-listen_to-event>) how to get this value.
2. With `event`, ControllerX listens to the changes of the event entity.
