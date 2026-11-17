# Sengled E1EG7F

![Sengled E1EG7F](<https://xaviml.github.io/controllerx/assets/controllers/E1EG7F.jpeg>)

- **Manufacturer:** Sengled
- **Device ID:** `E1EG7F`
- **Controller types:** [Light](<#light>) (`E1EG7FLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E1EG7FZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E1EG7F>)

## Light

- **Class:** `E1EG7FLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `"on"` | `"on"` | `on` |
| `on_long` | `on_long` | `click_color_up` |
| `on_double` | `on_double` | `on_full_color_temp` |
| `up` | `step_0_1_0` | `click_brightness_up` |
| `up_long` | `step_0_2_0` | `on_full_brightness` |
| `down` | `step_1_1_0` | `click_brightness_down` |
| `down_long` | `step_1_2_0` | `on_min_brightness` |
| `"off"` | `"off"` | `off` |
| `off_long` | `off_long` | `click_color_down` |
| `off_double` | `off_double` | `on_min_color_temp` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1EG7FLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1EG7FLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1EG7FLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E1EG7FZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `on_long` | `click_colortemp_up` |
| `on_double` | `on_full_color_temp` |
| `up` | `click_brightness_up` |
| `up_long` | `on_full_brightness` |
| `down` | `click_brightness_down` |
| `down_long` | `on_min_brightness` |
| `"off"` | `off` |
| `off_long` | `click_colortemp_down` |
| `off_double` | `on_min_color_temp` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1EG7FZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E1EG7FZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
