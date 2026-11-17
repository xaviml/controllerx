# Müller Licht MLI404011

![Müller Licht MLI404011](<https://xaviml.github.io/controllerx/assets/controllers/MLI404011.jpeg>)

- **Manufacturer:** Müller Licht
- **Device ID:** `MLI404011`
- **Controller types:** [Light](<#light>) (`MLI404011LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`MLI404011Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=MLI404011>)

## Notes

Some buttons are not mapped yet for either integration. Read more about it [here (deCONZ)](<https://github.com/xaviml/controllerx/issues/111>) and [here (z2m)](<https://github.com/xaviml/controllerx/issues/176>).

## Light

- **Class:** `MLI404011LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `"on"`, `"off"` | `1002` | `toggle` |
| `brightness_down_click` | `3002` | `click_brightness_down` |
| `brightness_down_hold` | `3001` | `hold_brightness_down` |
| `brightness_down_release`, `brightness_up_release` | `2003`, `3003` | `release` |
| `brightness_up_click` | `2002` | `click_brightness_up` |
| `brightness_up_hold` | `2001` | `hold_brightness_up` |
| `color_wheel` | `6002` | `xycolor_from_controller` |
| `color_temp` |  | `colortemp_from_controller` |
| `scene_1`, `scene_2`, `scene_3`, `scene_4`, `scene_5`, `scene_6` | `7002`, `8002`, `9002`, `10002`, `11002`, `12002` | *No action* |
|  | `4002` | `click_color_up` |
|  | `5002` | `click_color_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: MLI404011LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MLI404011LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MLI404011LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `MLI404011Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"`, `"off"` | `toggle` |
| `brightness_down_click` | `click_brightness_down` |
| `brightness_down_hold` | `hold_brightness_down` |
| `brightness_down_release`, `brightness_up_release` | `release` |
| `brightness_up_click` | `click_brightness_up` |
| `brightness_up_hold` | `hold_brightness_up` |
| `color_wheel` | `xycolor_from_controller` |
| `color_temp` | `colortemp_from_controller` |
| `scene_1`, `scene_2`, `scene_3`, `scene_4`, `scene_5`, `scene_6` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: MLI404011Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: MLI404011Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
