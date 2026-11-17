This integration (**`mqtt`**) listens to the MQTT topic set in the `controller` attribute. Although this integration is meant to be used with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>), it also works with the actions from Zigbee2MQTT.

ControllerX listens directly to MQTT rather than to Home Assistant. Not only can you use this with Zigbee2MQTT, but also with any other MQTT integration. This works for JSON and non-JSON payloads. If a specific attribute needs to be extracted from a JSON payload, the `key` parameter (which works like `action_key` in the Zigbee2MQTT integration) can be used.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `mqtt` |
| `key` | The key to retrieve the data from. | `-` |

*\* Required fields*

## How to extract the `controller` attribute

For MQTT, the `controller` attribute is the MQTT topic to listen to. Unless `key` is set, the payload of the topic must contain the action name directly, not JSON. This means that when using the MQTT integration with a Zigbee2MQTT controller, the topic to listen to must be `zigbee2mqtt/<friendly name>/action` or `zigbee2mqtt/<friendly name>/click`. You can see the topics in the Zigbee2MQTT logs.

## Example

```
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

This example turns on the light when the following payload is published to one of the 2 topics in the `controller` key:

```
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

Without `key`, the integration reads non-JSON payloads. Last but not least, the [MQTT plugin needs to be enabled](<https://xaviml.github.io/controllerx/others/enable-mqtt-plugin/index.md>).
