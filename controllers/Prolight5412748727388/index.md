# Prolight 5412748727388

![Prolight 5412748727388](<https://xaviml.github.io/controllerx/assets/controllers/Prolight5412748727388.jpeg>)

- **Manufacturer:** Prolight
- **Device ID:** `Prolight5412748727388`
- **Controller types:** [Light](<#light>) (`Prolight5412748727388LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`Prolight5412748727388Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=Prolight5412748727388>)

## Light

- **Class:** `Prolight5412748727388LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `brightness_move_to_level` | `brightness_from_controller_level` |
| `color_temperature_move` | `colortemp_from_controller` |
| `color_temperature_move_up` | `click_colortemp_up` |
| `color_temperature_move_down` | `click_colortemp_down` |
| `color_move` | `xycolor_from_controller` |

### Example configuration

```
example_app:
  module: controllerx
  class: Prolight5412748727388LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Prolight5412748727388LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `Prolight5412748727388Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `brightness_move_to_level` | `brightness_from_controller_level` |
| `color_temperature_move` | `colortemp_from_controller` |
| `color_temperature_move_up` | `click_colortemp_up` |
| `color_temperature_move_down` | `click_colortemp_down` |
| `color_move` | `xycolor_from_controller` |

### Example configuration

```
example_app:
  module: controllerx
  class: Prolight5412748727388Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: Prolight5412748727388Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
