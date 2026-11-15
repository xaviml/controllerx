---
title: Integrations
description: How ControllerX integrations work and which integrations are supported (Zigbee2MQTT, deCONZ, ZHA, Shelly, Tasmota, MQTT, state and custom events).
---

Integrations abstract how ControllerX receives the events from the controllers. Each integration is responsible for listening to a state, an event or an MQTT topic, and for decoding the controller events into actions that ControllerX understands.

These are the integrations supported by ControllerX.

### Integrations with mappings

These integrations have a default mapping for specific controllers (see [supported controllers](../../controllers/index.md)).

| Integration                                                      | Configuration value |
| ---------------------------------------------------------------- | ------------------- |
| [Zigbee2MQTT](zigbee2mqtt.md)       | `z2m`               |
| [deCONZ](deconz.md)                 | `deconz`            |
| [ZHA](zha.md)                       | `zha`               |
| [Homematic](homematic.md)           | `homematic`         |
| [Lutron Caséta](lutron_caseta.md)   | `lutron_caseta`     |
| [Shelly](shelly.md)                 | `shelly`            |
| [Shelly for HASS](shellyforhass.md) | `shellyforhass`     |
| [Tasmota](tasmota.md)               | `tasmota`           |

### Custom integrations

These integrations do not have a default mapping, so they are meant to be used with a [custom mapping](../../advanced/index.md).

| Integration                                    | Configuration value |
| ---------------------------------------------- | ------------------- |
| [State](state.md) | `state`             |
| [MQTT](mqtt.md)   | `mqtt`              |
| [Event](event.md) | `event`             |

## Example

The integration name can be placed directly in the `integration` parameter:

```yaml
example_app:
  module: controllerx
  ...
  integration: z2m
  ...
```

Or in the `name` parameter inside `integration`, in case you want to add other integration parameters:

```yaml
example_app:
  module: controllerx
  ...
  integration:
    name: z2m
    listen_to: mqtt
  ...
```
