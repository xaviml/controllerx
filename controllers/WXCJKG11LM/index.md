# Aqara WXCJKG11LM

![Aqara WXCJKG11LM](<https://xaviml.github.io/controllerx/assets/controllers/WXCJKG11LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXCJKG11LM`
- **Controller types:** [Light](<#light>) (`WXCJKG11LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXCJKG11LMZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXCJKG11LM>)

## Light

- **Class:** `WXCJKG11LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `button_1_single` | `1002` | `off` |
| `button_1_double` |  | `on_min_brightness` |
| `button_1_hold` | `1001` | `hold_brightness_down` |
| `button_1_release`, `button_2_release` | `1003`, `2003` | `release` |
| `button_2_single` | `2002` | `on` |
| `button_2_double` |  | `on_full_brightness` |
| `button_2_hold` | `2001` | `hold_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG11LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG11LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG11LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXCJKG11LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `button_1_single` | `off` |
| `button_1_double` | `on_min_brightness` |
| `button_1_hold` | `hold_brightness_down` |
| `button_1_release`, `button_2_release` | `release` |
| `button_2_single` | `on` |
| `button_2_double` | `on_full_brightness` |
| `button_2_hold` | `hold_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG11LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG11LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
