# RGB Genie ZB3009

![RGB Genie ZB3009](<https://xaviml.github.io/controllerx/assets/controllers/ZB3009.jpeg>)

- **Manufacturer:** RGB Genie
- **Device ID:** `ZB3009`
- **Controller types:** [Light](<#light>) (`ZB3009LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`ZB3009Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ZB3009>)

## Light

- **Class:** `ZB3009LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"`, `"off"` | `toggle` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `color_temperature_move_down` | `click_colortemp_down` |
| `color_temperature_move_up` | `click_colortemp_up` |
| `color_temperature_move` | `colortemp_from_controller` |
| `color_move` | `xycolor_from_controller` |
| `hue_move`, `recall_1`, `recall_3`, `recall_2` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: ZB3009LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ZB3009LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `ZB3009Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"`, `"off"` | `toggle` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `color_temperature_move_down` | `click_colortemp_down` |
| `color_temperature_move_up` | `click_colortemp_up` |
| `color_temperature_move` | `colortemp_from_controller` |
| `color_move` | `xycolor_from_controller` |
| `hue_move`, `recall_1`, `recall_3`, `recall_2` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: ZB3009Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: ZB3009Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
