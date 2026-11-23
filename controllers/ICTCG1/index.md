# IKEA ICTCG1

![IKEA ICTCG1](<https://xaviml.github.io/controllerx/assets/controllers/ICTCG1.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `ICTCG1`
- **Controller types:** [Light](<#light>) (`ICTCG1Controller`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`ICTCG1Z2MLightController`), [Media Player](<#media-player>) (`ICTCG1MediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ICTCG1>)

## Light

- **Class:** `ICTCG1Controller`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `brightness_move_up` |  | `move_with_on_off_0_70` | `hold_brightness_up` |
| `brightness_move_down` |  | `move_1_70`, `move_1_195` | `hold_brightness_down` |
| `brightness_stop` |  | `stop` | `release` |
| `brightness_move_to_level` |  |  | `brightness_from_controller_level` |
|  | `1002` | `move_to_level_with_on_off_255_1` | `rotate_right_quick` |
|  | `2002` |  | `click_brightness_up` |
|  | `3002` |  | `click_brightness_down` |
|  | `4002` | `move_to_level_with_on_off_0_1` | `rotate_left_quick` |
|  |  | `move_with_on_off_0_195` | `on` |

### Example configuration

```
example_app:
  module: controllerx
  class: ICTCG1Controller
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1Controller
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1Controller
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1Controller
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `ICTCG1Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `brightness_move_to_level` | `brightness_from_controller_level` |

### Example configuration

```
example_app:
  module: controllerx
  class: ICTCG1Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `ICTCG1MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `brightness_move_up` |  | `move_with_on_off_0_70`, `move_with_on_off_0_195` | `hold_volume_up` |
| `brightness_move_down` |  | `move_1_70`, `move_1_195` | `hold_volume_down` |
| `brightness_stop` |  | `stop` | `release` |
|  | `1002` | `move_to_level_with_on_off_255_1` | `rotate_right_quick` |
|  | `2002` |  | `click_volume_up` |
|  | `3002` |  | `click_volume_down` |
|  | `4002` | `move_to_level_with_on_off_0_1` | `rotate_left_quick` |

### Example configuration

```
example_app:
  module: controllerx
  class: ICTCG1MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1MediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: ICTCG1MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
