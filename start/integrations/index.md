Integrations abstract how ControllerX receives the events from the controllers. Each integration is responsible for listening to a state, an event or an MQTT topic, and for decoding the controller events into actions that ControllerX understands.

These are the integrations supported by ControllerX.

### Integrations with mappings

These integrations have a default mapping for specific controllers (see [supported controllers](<https://xaviml.github.io/controllerx/controllers/index.md>)).

| Integration | Configuration value |
| --- | --- |
| [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) | `z2m` |
| [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) | `deconz` |
| [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) | `zha` |
| [Homematic](<https://xaviml.github.io/controllerx/start/integrations/homematic/index.md>) | `homematic` |
| [Lutron Caséta](<https://xaviml.github.io/controllerx/start/integrations/lutron_caseta/index.md>) | `lutron_caseta` |
| [Shelly](<https://xaviml.github.io/controllerx/start/integrations/shelly/index.md>) | `shelly` |
| [Shelly for HASS](<https://xaviml.github.io/controllerx/start/integrations/shellyforhass/index.md>) | `shellyforhass` |
| [Tasmota](<https://xaviml.github.io/controllerx/start/integrations/tasmota/index.md>) | `tasmota` |

### Custom integrations

These integrations do not have a default mapping, so they are meant to be used with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Integration | Configuration value |
| --- | --- |
| [State](<https://xaviml.github.io/controllerx/start/integrations/state/index.md>) | `state` |
| [MQTT](<https://xaviml.github.io/controllerx/start/integrations/mqtt/index.md>) | `mqtt` |
| [Event](<https://xaviml.github.io/controllerx/start/integrations/event/index.md>) | `event` |

## Example

The integration name can be placed directly in the `integration` parameter:

```
example_app:
  module: controllerx
  ...
  integration: z2m
  ...
```

Or in the `name` parameter inside `integration`, in case you want to add other integration parameters:

```
example_app:
  module: controllerx
  ...
  integration:
    name: z2m
    listen_to: mqtt
  ...
```
