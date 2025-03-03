---
title: Zigbee2MQTT
layout: page
---

This integration (**`z2m`**) is meant to be used for zigbee2mqtt. It listens to the states from the HA sensor entities. These are the accepted attributes:

## Parameters

| Parameters     | Description                                                                                          | Default       |
| -------------- | ---------------------------------------------------------------------------------------------------- | ------------- |
| `name`         | Integration name                                                                                     | `z2m`         |
| `listen_to`    | Indicates whether it listens for HA states (`ha`), MQTT topics (`mqtt`) or HA Event state (`event`). | `ha`          |
| `action_key`   | The key inside the topic payload that contains the fired action from the controller.                 | `action`      |
| `action_group` | A list of allowed action groups for the controller configuration.                                    | `-`           |
| `topic_prefix` | MQTT base topic for Zigbee2MQTT MQTT messages.                                                       | `zigbee2mqtt` |

## How to extract the `controller` attribute

### HA States (`listen_to: ha`)

!!! warning

    This option is deprecated since ControllerX v4.29.0.

!!! note

    This option requires enabling `legacy_action_sensor` in Zigbee2MQTT. This can be done in Zigbee2MQTT `Settings > Home Assistant integration`. Then enable `Home Assistant legacy action sensors`. Note that this option is deprecated from Zigbee2MQTT 2.0 and will be removed in the future.

To extract the controller ID for Zigbee2MQTT, you can find it in `Configuration > Integrations > MQTT` and then select the controller. The parameter you need is the entity id of the sensor that by default finishes in `_action`.

### MQTT topics `listen_to: mqtt`

!!! note

    This option requires [enabling the MQTT plugin](/controllerx/others/enable-mqtt-plugin).

To use the `mqtt` option, the MQTT topic is the friendly name of the controller in Zigbee2MQTT. This friendly name can be found in the Zigbee2MQTT configuration for the specific device.

For example, if the MQTT topic is `zigbee2mqtt/livingroom_controller`, the friendly name (and `controller` attribute) of the controller would be `livingroom_controller`.

### Event state `listen_to: event`

!!! note

    This option requires enabling `experimental_event_entities` in Zigbee2MQTT. This can be done in Zigbee2MQTT `Settings > Home Assistant integration`. Then enable `Home Assistant experimental event entities`. Note that this option is experimental from Zigbee2MQTT 2.0.

To extract the controller ID for Zigbee2MQTT, you can find it in `Configuration > Integrations > MQTT` and then select the controller. The parameter you need is the entity id of the action event without the `event.` prefix. E.g. if the event is `event.livingroom_controller_action`, the `controller` attribute should be `livingroom_controller_action`.

## Example

Imagine we have the following configuration already created for a `z2m` controller listening to HA state:

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

Then, if we want to listen to the MQTT topic directly (skipping the HA state machine), we will need to change to:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
    action_key: action # By default is `action` already
  light: light.bedroom
```
