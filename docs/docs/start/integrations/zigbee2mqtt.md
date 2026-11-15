---
title: Zigbee2MQTT
description: Configure ControllerX with Zigbee2MQTT, listening to MQTT topics (recommended), Home Assistant event entities or the deprecated action sensors.
---

This integration (**`z2m`**) is meant to be used with Zigbee2MQTT. It can listen to MQTT topics directly (`listen_to: mqtt`, recommended), to Home Assistant event entities (`listen_to: event`) or to the deprecated Home Assistant action sensors (`listen_to: ha`).

## Parameters

| Parameters     | Description                                                                                          | Default       |
| -------------- | ---------------------------------------------------------------------------------------------------- | ------------- |
| `name`         | Integration name                                                                                     | `z2m`         |
| `listen_to`    | Indicates whether it listens for HA states (`ha`), MQTT topics (`mqtt`) or HA Event state (`event`). | `ha`          |
| `action_key`   | The key inside the topic payload that contains the fired action from the controller.                 | `action`      |
| `action_group` | A list of allowed action groups for the controller configuration.                                    | `-`           |
| `topic_prefix` | MQTT base topic for Zigbee2MQTT MQTT messages.                                                       | `zigbee2mqtt` |

## How to extract the `controller` attribute

### MQTT topics `listen_to: mqtt` { #mqtt-topics-listen_to-mqtt }

!!! note

    This option requires [enabling the MQTT plugin](../../others/enable-mqtt-plugin.md).

This is the recommended option. The `controller` attribute is the friendly name of the controller in Zigbee2MQTT, which can be found in the Zigbee2MQTT configuration of the device.

For example, if the MQTT topic is `zigbee2mqtt/livingroom_controller`, the friendly name (and `controller` attribute) of the controller would be `livingroom_controller`.

### Event state `listen_to: event` { #event-state-listen_to-event }

!!! note

    This option requires enabling `experimental_event_entities` in Zigbee2MQTT. This can be done in Zigbee2MQTT `Settings > Home Assistant integration`. Then enable `Home Assistant experimental event entities`. Note that this option is experimental since Zigbee2MQTT 2.0.

To find the controller ID for Zigbee2MQTT, go to `Settings > Devices & services > MQTT` and select the controller. The parameter you need is the entity ID of the action event without the `event.` prefix. E.g. if the event is `event.livingroom_controller_action`, the `controller` attribute should be `livingroom_controller_action`.

### HA States (`listen_to: ha`, deprecated) { #ha-states-listen_to-ha }

!!! warning

    This option is deprecated since ControllerX v4.29.0.

!!! note

    This option requires enabling `legacy_action_sensor` in Zigbee2MQTT. This can be done in Zigbee2MQTT `Settings > Home Assistant integration`. Then enable `Home Assistant legacy action sensors`. Note that this option is deprecated since Zigbee2MQTT 2.0 and will be removed in the future.

To find the controller ID for Zigbee2MQTT, go to `Settings > Devices & services > MQTT` and select the controller. The parameter you need is the entity ID of the sensor that by default finishes in `_action`.

## Example

Imagine we have the following configuration already created for a `z2m` controller listening to the (deprecated) HA state:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration:
    name: z2m
    listen_to: ha
  light: light.bedroom
```

Then, if we want to listen to the MQTT topic directly (skipping the HA state machine), we need to change it to:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
    action_key: action # `action` by default
  light: light.bedroom
```
