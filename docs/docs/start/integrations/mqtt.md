---
title: MQTT
layout: page
---

This integration (**`mqtt`**) listens for the topic sent from the `controller` attribute. Although this integration makes sense to use together with [custom controllers](/controllerx/advanced), it works with the actions from zigbee2mqtt.

ControllerX will be listening directly from MQTT rather than Home Assistant (which listens from MQTT). Not only can you use this with zigbee2mqtt, but also with any other MQTT integration. This works for JSON and non-JSON values in the payload. If a specific attribute needs to be extracted from JSON payload, the `key` (which works like `action_key` from Zigbee2MQTT integration) attribute can be used:

## Parameters

| Parameter | Description                        | Default |
| --------- | ---------------------------------- | ------- |
| `name`\*  | Integration name.                  | `mqtt`  |
| `key`     | The key to retrieve the data from. | `-`     |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for MQTT, the `controller` attribute must have the MQTT topic to listen from. It is important that the topic payload contains directly the action name and not a JSON. This means that in case of using the MQTT integration with a z2m controller, then the topic to listen to must be `zigbee2mqtt/<friendly name>/action` or `zigbee2mqtt/<friendly name>/click`. You can see the topic on the Zigbee2MQTT logs.

## Example

```yaml
example_app:
  module: controllerx
  class: LightController
  controller:
    - zigbee2mqtt/stairway_sensor01_occupancy
    - zigbee2mqtt/stairway_sensor02_occupancy
  light: light.stairway
  integration:
    name: mqtt
    key: occupancy
  mapping:
    "true": "on"
    "false": "off"
```

This example will turn on the light when the following payload is shown for one of the 2 topics in the `controller` key:

```json
{
  "battery": 99,
  "illuminance": 0,
  "illuminance_lux": 0,
  "linkquality": 255,
  "occupancy": true,
  "temperature": 27,
  "voltage": 2985
}
```

By default, mqtt will read non-JSON values. Last but not least, the [MQTT plugin needs to be enabled](/controllerx/others/enable-mqtt-plugin).
