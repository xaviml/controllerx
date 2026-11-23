# ADEO HRC99CZC045

![ADEO HRC99CZC045](<https://xaviml.github.io/controllerx/assets/controllers/AdeoHRC99CZC045.jpeg>)

- **Manufacturer:** ADEO
- **Device ID:** `AdeoHRC99CZC045`
- **Controller types:** [Light](<#light>) (`AdeoHRC99CZC045LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`AdeoHRC99CZC045Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=AdeoHRC99CZC045>)

## Light

- **Class:** `AdeoHRC99CZC045LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_step_up` | `hold_brightness_up` |
| `brightness_step_down` | `hold_brightness_down` |
| `brightness_stop`, `color_stop` | `release` |
| `color_hue_step_up`, `color_saturation_step_up` | `hold_color_up` |
| `color_hue_step_down`, `color_saturation_step_down` | `hold_color_down` |
| `color_temperature_step_up` | `hold_colortemp_up` |
| `color_temperature_step_down` | `hold_colortemp_down` |
| `scene_1`, `scene_2`, `scene_3`, `scene_4` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: AdeoHRC99CZC045LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: AdeoHRC99CZC045LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `AdeoHRC99CZC045Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_step_up` | `hold_brightness_up` |
| `brightness_step_down` | `hold_brightness_down` |
| `brightness_stop`, `color_stop` | `release` |
| `color_hue_step_up`, `color_saturation_step_up`, `color_temperature_step_up` | `hold_colortemp_up` |
| `color_hue_step_down`, `color_saturation_step_down`, `color_temperature_step_down` | `hold_colortemp_down` |
| `scene_1`, `scene_2`, `scene_3`, `scene_4` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: AdeoHRC99CZC045Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: AdeoHRC99CZC045Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
