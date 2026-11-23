# SONOFF SNZB01

![SONOFF SNZB01](<https://xaviml.github.io/controllerx/assets/controllers/SNZB01.jpeg>)

- **Manufacturer:** SONOFF
- **Device ID:** `SNZB01`
- **Controller types:** [Light](<#light>) (`SNZB01LightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=SNZB01>)

## Light

- **Class:** `SNZB01LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `single` | `toggle` | `toggle` |
| `double` | `"on"` | `on_full_brightness` |
| `long` | `"off"` | `on_min_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: SNZB01LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: SNZB01LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: SNZB01LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
