# IKEA E1810

![IKEA E1810](<https://xaviml.github.io/controllerx/assets/controllers/E1810.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E1810`
- **Controller types:** [Light](<#light>) (`E1810Controller`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E1810Z2MLightController`), [Media Player](<#media-player>) (`E1810MediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E1810>)

## Notes

This device mapping also supports the E1524 controller.

## Light

- **Class:** `E1810Controller`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `toggle` | `1002` | `toggle` | `toggle` |
| `toggle_hold` | `1001` | `press_2_0_0` | `sync` |
| `brightness_up_click` | `2002` | `step_with_on_off_0_43_5` | `click_brightness_up` |
| `brightness_down_click` | `3002` | `step_1_43_5_0_0` | `click_brightness_down` |
| `arrow_left_click` | `4002` | `press_257_13_0` | `click_color_down` |
| `arrow_right_click` | `5002` | `press_256_13_0` | `click_color_up` |
| `brightness_up_hold` | `2001` | `move_with_on_off_0_83`, `move_with_on_off_0_84` | `hold_brightness_up` |
| `brightness_up_release`, `brightness_down_release`, `arrow_left_release`, `arrow_right_release` | `2003`, `3003`, `4003`, `5003` | `stop`, `stop_with_on_off`, `release` | `release` |
| `brightness_down_hold` | `3001` | `move_1_83_0_0`, `move_1_84_0_0` | `hold_brightness_down` |
| `arrow_left_hold` | `4001` | `hold_3329_0` | `hold_color_down` |
| `arrow_right_hold` | `5001` | `hold_3328_0` | `hold_color_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1810Controller
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810Controller
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810Controller
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810Controller
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E1810Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `toggle` | `toggle` |
| `toggle_hold` | `on_full_brightness` |
| `brightness_up_click` | `click_brightness_up` |
| `brightness_down_click` | `click_brightness_down` |
| `arrow_left_click` | `click_colortemp_down` |
| `arrow_right_click` | `click_colortemp_up` |
| `brightness_up_hold` | `hold_brightness_up` |
| `brightness_up_release`, `brightness_down_release`, `arrow_left_release`, `arrow_right_release` | `release` |
| `brightness_down_hold` | `hold_brightness_down` |
| `arrow_left_hold` | `hold_colortemp_down` |
| `arrow_right_hold` | `hold_colortemp_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1810Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `E1810MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `toggle` | `1002` | `toggle` | `play_pause` |
| `brightness_up_click` | `2002` | `step_with_on_off_0_43_5` | `click_volume_up` |
| `brightness_down_click` | `3002` | `step_1_43_5_0_0` | `click_volume_down` |
| `arrow_left_click` | `4002` | `press_257_13_0` | `previous_track` |
| `arrow_right_click` | `5002` | `press_256_13_0` | `next_track` |
| `arrow_left_hold` | `4001` | `hold_3329_0` | `previous_source` |
| `arrow_right_hold` | `5001` | `hold_3328_0` | `next_source` |
| `brightness_up_hold` | `2001` | `move_with_on_off_0_83`, `move_with_on_off_0_84` | `hold_volume_up` |
| `brightness_up_release`, `brightness_down_release` | `2003`, `3003` | `stop`, `stop_with_on_off`, `release` | `release` |
| `brightness_down_hold` | `3001` | `move_1_83_0_0`, `move_1_84_0_0` | `hold_volume_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1810MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810MediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1810MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
