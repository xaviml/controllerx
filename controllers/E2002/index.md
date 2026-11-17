# IKEA E2002

![IKEA E2002](<https://xaviml.github.io/controllerx/assets/controllers/E2002.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E2002`
- **Controller types:** [Light](<#light>) (`E2002LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E2002Z2MLightController`), [Media Player](<#media-player>) (`E2002MediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E2002>)

## Notes

This controller fires the "on" action when the arrows are held, as well as the hold arrow action. This means that when long pressing the arrows, the light(s) will turn on before changing the color.

This device mapping also supports the E2001 controller.

## Light

- **Class:** `E2002LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `on` |
| `"off"` | `2002` | `"off"` | `off` |
| `arrow_left_click` | `3002` | `press_257_13_0` | `click_color_down` |
| `arrow_right_click` | `4002` | `press_256_13_0` | `click_color_up` |
| `brightness_move_up` | `1001` | `move_with_on_off_0_83` | `hold_brightness_up` |
| `brightness_stop`, `arrow_left_release`, `arrow_right_release` | `1003`, `2003`, `3003`, `4003` | `stop`, `stop_with_on_off`, `release` | `release` |
| `brightness_move_down` | `2001` | `move_1_83_0_0` | `hold_brightness_down` |
| `arrow_left_hold` | `3001` | `hold_3329_0` | `hold_color_down` |
| `arrow_right_hold` | `4001` | `hold_3328_0` | `hold_color_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: E2002LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E2002Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `arrow_left_click` | `click_colortemp_down` |
| `arrow_right_click` | `click_colortemp_up` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_stop`, `arrow_left_release`, `arrow_right_release` | `release` |
| `brightness_move_down` | `hold_brightness_down` |
| `arrow_left_hold` | `hold_colortemp_down` |
| `arrow_right_hold` | `hold_colortemp_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: E2002Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `E2002MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `play_pause` |
| `"off"` | `2002` | `"off"` | `click_volume_down` |
| `arrow_left_click` | `3002` | `press_257_13_0` | `previous_track` |
| `arrow_right_click` | `4002` | `press_256_13_0` | `next_track` |
| `arrow_left_hold` | `3001` | `hold_3329_0` | `previous_source` |
| `arrow_left_release`, `arrow_right_release`, `brightness_stop` | `1003`, `2003`, `3003`, `4003` | `stop`, `stop_with_on_off`, `release` | `release` |
| `arrow_right_hold` | `4001` | `hold_3328_0` | `next_source` |
| `brightness_move_up` | `1001` | `move_with_on_off_0_83` | `hold_volume_up` |
| `brightness_move_down` | `2001` | `move_1_83_0_0` | `hold_volume_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: E2002MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002MediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2002MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
