# Aqara WXKG12LM

![Aqara WXKG12LM](<https://xaviml.github.io/controllerx/assets/controllers/WXKG12LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG12LM`
- **Controller types:** [Light](<#light>) (`WXKG12LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXKG12LMZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG12LM>)

## Light

- **Class:** `WXKG12LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `single` | `1002` | `toggle` |
| `double` | `1004` | `on_full_brightness` |
| `shake` | `1007` | `on_min_brightness` |
| `hold` | `1001` | `hold_brightness_toggle` |
| `release` | `1003` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG12LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG12LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG12LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXKG12LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `single` | `toggle` |
| `double` | `on_full_brightness` |
| `shake` | `on_min_brightness` |
| `hold` | `hold_brightness_toggle` |
| `release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG12LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG12LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
