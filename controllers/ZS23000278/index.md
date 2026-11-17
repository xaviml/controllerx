# Linkind ZS23000278

![Linkind ZS23000278](<https://xaviml.github.io/controllerx/assets/controllers/ZS23000278.jpeg>)

- **Manufacturer:** Linkind
- **Device ID:** `ZS23000278`
- **Controller types:** [Light](<#light>) (`ZS23000278LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`ZS23000278Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ZS23000278>)

## Light

- **Class:** `ZS23000278LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_step_up` | `click_brightness_up` |
| `brightness_step_down` | `click_brightness_down` |
| `brightness_move_to_level` | `brightness_from_controller_level` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `color_temperature_move` | `colortemp_from_controller` |
| `color_temperature_move_up` | `click_colortemp_up` |
| `color_temperature_move_down` | `click_colortemp_down` |
| `color_move` | `xycolor_from_controller` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZS23000278LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ZS23000278LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `ZS23000278Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_step_up` | `click_brightness_up` |
| `brightness_step_down` | `click_brightness_down` |
| `brightness_move_to_level` | `brightness_from_controller_level` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `color_temperature_move` | `colortemp_from_controller` |
| `color_temperature_move_up` | `click_colortemp_up` |
| `color_temperature_move_down` | `click_colortemp_down` |
| `color_move` | `xycolor_from_controller` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZS23000278Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: ZS23000278Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
