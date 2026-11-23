# Legrand 600088

![Legrand 600088](<https://xaviml.github.io/controllerx/assets/controllers/Legrand600088.jpeg>)

- **Manufacturer:** Legrand
- **Device ID:** `Legrand600088`
- **Controller types:** [Light](<#light>) (`Legrand600088LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`Legrand600088Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=Legrand600088>)

## Light

- **Class:** `Legrand600088LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `on_left` | `1_on` | `on` |
| `off_left` | `1_off` | `off` |
| `brightness_move_up_left` | `1_move_up` | `hold_color_up` |
| `brightness_move_down_left` | `1_move_down` | `hold_color_down` |
| `brightness_stop_left`, `brightness_stop_right` | `1_stop`, `2_stop` | `release` |
| `on_right` | `2_on` | `on_full_brightness` |
| `off_right` | `2_off` | `on_min_brightness` |
| `brightness_move_up_right` | `2_move_up` | `hold_brightness_up` |
| `brightness_move_down_right` | `2_move_down` | `hold_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: Legrand600088LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Legrand600088LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Legrand600088LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `Legrand600088Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `on_left` | `on` |
| `off_left` | `off` |
| `brightness_move_up_left` | `hold_colortemp_up` |
| `brightness_move_down_left` | `hold_colortemp_down` |
| `brightness_stop_left`, `brightness_stop_right` | `release` |
| `on_right` | `on_full_brightness` |
| `off_right` | `on_min_brightness` |
| `brightness_move_up_right` | `hold_brightness_up` |
| `brightness_move_down_right` | `hold_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: Legrand600088Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: Legrand600088Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
