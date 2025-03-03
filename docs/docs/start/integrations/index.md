---
title: Integrations
layout: page
---

Integrations are a way to abstract the logic from the event extraction in ControllerX. Each integration is responsible for listening to the state or event and decoding the events from controllers in a way that ControllerX understands.

These are the integrations supported by ControllerX.

### Integrations with mappings

These are integrations with default mapping for specific controllers.

| Integration                                                      | Configuration value |
| ---------------------------------------------------------------- | ------------------- |
| [Zigbee2MQTT](/controllerx/start/integrations/zigbee2mqtt)       | `z2m`               |
| [deCONZ](/controllerx/start/integrations/deconz)                 | `deconz`            |
| [ZHA](/controllerx/start/integrations/zha)                       | `zha`               |
| [Homematic](/controllerx/start/integrations/homematic)           | `homematic`         |
| [Lutron Caséta](/controllerx/start/integrations/lutron_caseta)   | `lutron_caseta`     |
| [Shelly](/controllerx/start/integrations/shelly)                 | `shelly`            |
| [Shelly for HASS](/controllerx/start/integrations/shellyforhass) | `shellyforhass`     |

### Custom integrations

These are integrations that do not require a default mapping. Designed for custom soltions.

| Integration                                    | Configuration value |
| ---------------------------------------------- | ------------------- |
| [State](/controllerx/start/integrations/state) | `state`             |
| [MQTT](/controllerx/start/integrations/mqtt)   | `mqtt`              |
| [Event](/controllerx/start/integrations/event) | `event`             |

## Example

One could place the configuration name directly in the integration parameter:

```yaml
example_app:
  module: controllerx
  ...
  integration: z2m
  ...
```

Or in the `name` parameter inside `integration` in case you want to add other integration parameters:

```yaml
example_app:
  module: controllerx
  ...
  integration:
    name: z2m
  ...
```
