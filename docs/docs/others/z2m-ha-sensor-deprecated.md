---
title: Zigbee2MQTT - HA sensor is deprecated
layout: page
---

_Zigbee2MQTT HA sensor deprecated since ControllerX v4.29.0_

Zigbee2MQTT 2.0.0 brought [some breaking changes](https://github.com/Koenkk/zigbee2mqtt/discussions/24198), and one of them was to deprecate the [Home Assistant action sensors](https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html#via-home-assistant-action-sensor-deprecated), which is the default option for [Zigbee2MQTT integration](/controllerx/start/integrations/zigbee2mqtt) in ControllerX.

You might be here because of a warning in AppDaemon logs that look like the following:

!!! quote

    ⚠️ Listening to HA sensor actions is now deprecated and will be removed in the future. Use `listen_to: mqtt` or `listen_to: event` instead. Read more about it here: https://xaviml.github.io/controllerx/others/z2m-ha-sensor-deprecated

This might be because your controller configuration looks like:

```yaml hl_lines="4-5"
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
```

The issue is within the `integration: z2m` which is defaulted to read a HA `sensor`. You need to switch to either [`mqtt`](/controllerx/start/integrations/zigbee2mqtt/#mqtt-topics-listen_to-mqtt) (recommended) or HA [`event`](/controllerx/start/integrations/zigbee2mqtt/#event-state-listen_to-event) (experimental).

## Switch to MQTT listener (recommended)

In case of switching to MQTT (as [recommneded by Zigbee2MQTT](https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html#via-mqtt-device-trigger-recommended)), you would need to first [enable MQTT plugin](/controllerx/others/enable-mqtt-plugin). Then, change your configuration to something like the following:

```yaml hl_lines="4-7"
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller # (1)
  integration:
    name: z2m
    listen_to: mqtt # (2)
  light: light.livingroom
```

1. This is the device friendly_name in Zigbee2MQTT. Check [here](/controllerx/start/integrations/zigbee2mqtt/#mqtt-topics-listen_to-mqtt) how to get this value.
2. By indicating `mqtt` here, ControllerX will listen to MQTT controller topic.

## Switch to HA Event sensor listener (experimental)

Another option is to listen the newly (and experimental) event entity from Zigbee2MQTT 2.0.0. First, we will need to enable the experimental feature in Zigbee2MQTT as explained [here](/controllerx/start/integrations/zigbee2mqtt/#event-state-listen_to-event). Then, you would need to switch configuration to something like:

```yaml hl_lines="4-7"
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: office_controller_action # (1)
  integration:
    name: z2m
    listen_to: event # (2)
  light: light.livingroom
```

1. This is the event entity without the `event.` prefix. Check [here](/controllerx/start/integrations/zigbee2mqtt/#event-state-listen_to-event) how to get this value.
2. By indicating `event` here, ControllerX will listen to the event entity changes.
