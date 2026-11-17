# IKEA E2213

![IKEA E2213](<https://xaviml.github.io/controllerx/assets/controllers/E2213.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E2213`
- **Controller types:** [Light](<#light>) (`E2213LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E2213Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E2213>)

## Light

- **Class:** `E2213LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1_long_press` | `hold_brightness_up` |
| `2_long_press` | `hold_brightness_down` |
| `1_short_release` | `on` |
| `2_short_release` | `off` |
| `1_long_release`, `2_long_release` | `release` |
| `1_double_press` | `hold_color_up` |
| `2_double_press` | `hold_color_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: E2213LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2213LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E2213Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `1_long_press` | `hold_brightness_up` |
| `2_long_press` | `hold_brightness_down` |
| `1_short_release` | `on` |
| `2_short_release` | `off` |
| `1_long_release`, `2_long_release` | `release` |
| `1_double_press` | `hold_colortemp_up` |
| `2_double_press` | `hold_colortemp_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: E2213Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E2213Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
