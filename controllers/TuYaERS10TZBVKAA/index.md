# Tuya ERS10TZBVKAA

![Tuya ERS10TZBVKAA](<https://xaviml.github.io/controllerx/assets/controllers/TuYaERS10TZBVKAA.jpeg>)

- **Manufacturer:** Tuya
- **Device ID:** `TuYaERS10TZBVKAA`
- **Controller types:** [Light](<#light>) (`TuYaERS10TZBVKAALightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`TuYaERS10TZBVKAAZ2MLightController`), [Media Player](<#media-player>) (`TuYaERS10TZBVKAAMediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TuYaERS10TZBVKAA>)

## Light

- **Class:** `TuYaERS10TZBVKAALightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `brightness_step_up`, `rotate_right` |  | `click_brightness_up` |
| `brightness_step_down`, `rotate_left` |  | `click_brightness_down` |
| `toggle`, `single` | `toggle` | `toggle` |
| `hue_move` |  | `hold_brightness_toggle` |
| `hue_stop` |  | `release` |
| `color_temperature_step_up` |  | `click_color_up` |
| `color_temperature_step_down` |  | `click_color_down` |
| `double` |  | `on_full_brightness` |
| `hold` |  | `on_min_brightness` |
|  | `step_brightness` | `brightness_from_controller_step` |
|  | `step_color_temp` | `colortemp_from_controller_step` |

### Example configuration

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAALightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAALightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAALightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `TuYaERS10TZBVKAAZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `brightness_step_up`, `rotate_right` | `click_brightness_up` |
| `brightness_step_down`, `rotate_left` | `click_brightness_down` |
| `toggle`, `single` | `toggle` |
| `hue_move` | `hold_brightness_toggle` |
| `hue_stop` | `release` |
| `color_temperature_step_up` | `click_colortemp_up` |
| `color_temperature_step_down` | `click_colortemp_down` |
| `double` | `on_full_brightness` |
| `hold` | `on_min_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAAZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAAZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `TuYaERS10TZBVKAAMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- |
| `brightness_step_up`, `rotate_right` | `click_volume_up` |
| `brightness_step_down`, `rotate_left` | `click_volume_down` |
| `toggle`, `single` | `play_pause` |
| `hue_move` | `hold_volume_up` |
| `hue_stop` | `release` |
| `color_temperature_step_up`, `double` | `next_track` |
| `color_temperature_step_down`, `hold` | `previous_track` |

### Example configuration

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAAMediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: TuYaERS10TZBVKAAMediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```
