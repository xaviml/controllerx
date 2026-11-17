# Philips RDM002

![Philips RDM002](<https://xaviml.github.io/controllerx/assets/controllers/PhilipsRDM002.jpeg>)

- **Manufacturer:** Philips
- **Device ID:** `PhilipsRDM002`
- **Controller types:** [Light](<#light>) (`PhilipsRDM002LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`PhilipsRDM002Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=PhilipsRDM002>)

## Light

- **Class:** `PhilipsRDM002LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `button_1_press_release` | `off` |
| `button_1_hold` | `hold_brightness_down` |
| `button_1_hold_release`, `button_2_hold_release`, `button_3_hold_release`, `button_4_hold_release` | `release` |
| `button_2_press_release` | `on` |
| `button_2_hold` | `hold_brightness_up` |
| `button_3_press_release` | `click_color_down` |
| `button_3_hold` | `hold_color_down` |
| `button_4_press_release` | `click_color_up` |
| `button_4_hold` | `hold_color_up` |
| `dial_rotate_left_step` | `click_brightness_down` |
| `dial_rotate_left_slow` | `on_min_color_temp` |
| `dial_rotate_left_fast` | `on_min_brightness` |
| `dial_rotate_right_step` | `click_brightness_up` |
| `dial_rotate_right_slow` | `on_full_color_temp` |
| `dial_rotate_right_fast` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: PhilipsRDM002LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: PhilipsRDM002LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `PhilipsRDM002Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `button_1_press_release` | `off` |
| `button_1_hold` | `hold_brightness_down` |
| `button_1_hold_release`, `button_2_hold_release`, `button_3_hold_release`, `button_4_hold_release` | `release` |
| `button_2_press_release` | `on` |
| `button_2_hold` | `hold_brightness_up` |
| `button_3_press_release` | `click_colortemp_down` |
| `button_3_hold` | `hold_colortemp_down` |
| `button_4_press_release` | `click_colortemp_up` |
| `button_4_hold` | `hold_colortemp_up` |
| `dial_rotate_left_step` | `click_brightness_down` |
| `dial_rotate_left_slow` | `on_min_color_temp` |
| `dial_rotate_left_fast` | `on_min_brightness` |
| `dial_rotate_right_step` | `click_brightness_up` |
| `dial_rotate_right_slow` | `on_full_color_temp` |
| `dial_rotate_right_fast` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: PhilipsRDM002Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: PhilipsRDM002Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
