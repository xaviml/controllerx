# Aqara WXCJKG12LM

![Aqara WXCJKG12LM](<https://xaviml.github.io/controllerx/assets/controllers/WXCJKG12LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXCJKG12LM`
- **Controller types:** [Light](<#light>) (`WXCJKG12LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXCJKG12LMZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXCJKG12LM>)

## Light

- **Class:** `WXCJKG12LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `button_1_single` | `1_single` | `off` |
| `button_1_double` | `1_double` | `on_min_color_temp` |
| `button_1_triple`, `button_2_triple`, `button_3_triple`, `button_4_triple` | `1_triple`, `2_triple`, `3_triple`, `4_triple` | *No action* |
| `button_1_hold` | `1_long press` | `hold_color_down` |
| `button_1_release`, `button_2_release`, `button_3_release`, `button_4_release` | `1_release`, `2_release`, `3_release`, `4_release` | `release` |
| `button_2_single` | `2_single` | `on` |
| `button_2_double` | `2_double` | `on_full_color_temp` |
| `button_2_hold` | `2_long press` | `hold_color_up` |
| `button_3_single` | `3_single` | `click_brightness_down` |
| `button_3_double` | `3_double` | `on_min_brightness` |
| `button_3_hold` | `3_long press` | `hold_brightness_down` |
| `button_4_single` | `4_single` | `click_brightness_up` |
| `button_4_double` | `4_double` | `on_full_brightness` |
| `button_4_hold` | `4_long press` | `hold_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG12LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG12LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG12LMLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXCJKG12LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `button_1_single` | `off` |
| `button_1_double` | `on_min_color_temp` |
| `button_1_triple`, `button_2_triple`, `button_3_triple`, `button_4_triple` | *No action* |
| `button_1_hold` | `hold_colortemp_down` |
| `button_1_release`, `button_2_release`, `button_3_release`, `button_4_release` | `release` |
| `button_2_single` | `on` |
| `button_2_double` | `on_full_color_temp` |
| `button_2_hold` | `hold_colortemp_up` |
| `button_3_single` | `click_brightness_down` |
| `button_3_double` | `on_min_brightness` |
| `button_3_hold` | `hold_brightness_down` |
| `button_4_single` | `click_brightness_up` |
| `button_4_double` | `on_full_brightness` |
| `button_4_hold` | `hold_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG12LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG12LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
