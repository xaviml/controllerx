# Aqara WXCJKG13LM

![Aqara WXCJKG13LM](<https://xaviml.github.io/controllerx/assets/controllers/WXCJKG13LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXCJKG13LM`
- **Controller types:** [Light](<#light>) (`WXCJKG13LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXCJKG13LMZ2MLightController`), [Media Player](<#media-player>) (`WXCJKG13LMMediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXCJKG13LM>)

## Light

- **Class:** `WXCJKG13LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `button_1_single` | `1002` | `1_single` | `off` |
| `button_1_double`, `button_2_double` | `1004`, `2004` | `1_double`, `2_double` | `sync` |
| `button_1_triple`, `button_1_hold`, `button_1_release`, `button_2_triple`, `button_2_hold`, `button_2_release`, `button_3_triple`, `button_4_triple`, `button_5_triple`, `button_6_triple` | `1005`, `1001`, `1003`, `2005`, `2001`, `2003`, `3005`, `4005`, `5005`, `6005` | `1_triple`, `1_long`, `1_release`, `2_triple`, `2_long`, `2_release`, `3_triple`, `4_triple`, `5_triple`, `6_triple` | *No action* |
| `button_2_single` | `2002` | `2_single` | `on` |
| `button_3_single` | `3002` | `3_single` | `click_brightness_down` |
| `button_3_double` | `3004` | `3_double` | `on_min_brightness` |
| `button_3_hold` | `3001` | `3_long` | `hold_brightness_down` |
| `button_3_release`, `button_4_release`, `button_5_release`, `button_6_release` | `3003`, `4003`, `5003`, `6003` | `3_release`, `4_release`, `5_release`, `6_release` | `release` |
| `button_4_single` | `4002` | `4_single` | `click_brightness_up` |
| `button_4_double` | `4004` | `4_double` | `on_full_brightness` |
| `button_4_hold` | `4001` | `4_long` | `hold_brightness_up` |
| `button_5_single` | `5002` | `5_single` | `click_color_down` |
| `button_5_double` | `5004` | `5_double` | `on_min_color_temp` |
| `button_5_hold` | `5001` | `5_long` | `hold_color_down` |
| `button_6_single` | `6002` | `6_single` | `click_color_up` |
| `button_6_double` | `6004` | `6_double` | `on_full_color_temp` |
| `button_6_hold` | `6001` | `6_long` | `hold_color_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG13LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXCJKG13LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `button_1_single` | `off` |
| `button_1_double`, `button_2_double`, `button_4_double` | `on_full_brightness` |
| `button_1_triple`, `button_1_hold`, `button_1_release`, `button_2_triple`, `button_2_hold`, `button_2_release`, `button_3_triple`, `button_4_triple`, `button_5_triple`, `button_6_triple` | *No action* |
| `button_2_single` | `on` |
| `button_3_single` | `click_brightness_down` |
| `button_3_double` | `on_min_brightness` |
| `button_3_hold` | `hold_brightness_down` |
| `button_3_release`, `button_4_release`, `button_5_release`, `button_6_release` | `release` |
| `button_4_single` | `click_brightness_up` |
| `button_4_hold` | `hold_brightness_up` |
| `button_5_single` | `click_colortemp_down` |
| `button_5_double` | `on_min_color_temp` |
| `button_5_hold` | `hold_colortemp_down` |
| `button_6_single` | `click_colortemp_up` |
| `button_6_double` | `on_full_color_temp` |
| `button_6_hold` | `hold_colortemp_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG13LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `WXCJKG13LMMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `button_1_single` | `1002` | `1_single` | `click_volume_down` |
| `button_1_double` | `1004` | `1_double` | `mute` |
| `button_1_triple`, `button_2_triple`, `button_3_double`, `button_3_triple`, `button_3_hold`, `button_3_release`, `button_4_double`, `button_4_triple`, `button_4_hold`, `button_4_release`, `button_5_double`, `button_5_triple`, `button_5_hold`, `button_5_release`, `button_6_double`, `button_6_triple`, `button_6_hold`, `button_6_release` | `1005`, `2005`, `3001`, `3003`, `3004`, `3005`, `4001`, `4003`, `4004`, `4005`, `5001`, `5003`, `5004`, `5005`, `6001`, `6003`, `6004`, `6005` | `1_triple`, `2_triple`, `3_double`, `3_triple`, `3_long`, `3_release`, `4_double`, `4_triple`, `4_long`, `4_release`, `5_double`, `5_triple`, `5_long`, `6_double`, `6_triple`, `6_long`, `6_release` | *No action* |
| `button_1_hold` | `1001` | `1_long` | `hold_volume_down` |
| `button_1_release`, `button_2_release` | `1003`, `2003` | `1_release`, `2_release`, `5_release` | `release` |
| `button_2_single` | `2002` | `2_single` | `click_volume_up` |
| `button_2_double` | `2004` | `2_double` | `play_pause` |
| `button_2_hold` | `2001` | `2_long` | `hold_volume_up` |
| `button_3_single` | `3002` | `3_single` | `previous_track` |
| `button_4_single` | `4002` | `4_single` | `next_track` |
| `button_5_single` | `5002` | `5_single` | `previous_source` |
| `button_6_single` | `6002` | `6_single` | `next_source` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXCJKG13LMMediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMMediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMMediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXCJKG13LMMediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
