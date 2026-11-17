# IKEA E1744

![IKEA E1744](<https://xaviml.github.io/controllerx/assets/controllers/E1744.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E1744`
- **Controller types:** [Light](<#light>) (`E1744LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E1744Z2MLightController`), [Media Player](<#media-player>) (`E1744MediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E1744>)

## Notes

If you want to use the default controller, you will need to set `legacy: false` in the Zigbee2MQTT configuration. Read more [here](<https://www.zigbee2mqtt.io/devices/E1744.html#legacy-integration>).

## Light

- **Class:** `E1744LightController`
- **Entity parameter:** `light`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `brightness_move_down` | `3001` | `move_1_195_0_0` | `hold_brightness_down` |
| `brightness_move_up` | `2001` | `move_0_195_0_0` | `hold_brightness_up` |
| `brightness_stop` | `2003`, `3003` | `stop` | `release` |
| `toggle` | `1002` | `toggle` | `toggle` |
| `brightness_step_up` | `1004` | `step_0_1_0_0_0` | `on_full_brightness` |
| `brightness_step_down` | `1005` | `step_1_1_0_0_0` | `on_min_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1744LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E1744Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_stop` | `release` |
| `toggle` | `toggle` |
| `brightness_step_up` | `on_full_brightness` |
| `brightness_step_down` | `on_min_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1744Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `E1744MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `brightness_move_down` | `3001` | `move_1_195_0_0` | `hold_volume_down` |
| `brightness_move_up` | `2001` | `move_0_195_0_0` | `hold_volume_up` |
| `brightness_stop` | `2003`, `3003` | `stop` | `release` |
| `toggle` | `1002` | `toggle` | `play_pause` |
| `brightness_step_up` | `1004` | `step_0_1_0_0_0` | `next_track` |
| `brightness_step_down` | `1005` | `step_1_1_0_0_0` | `previous_track` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1744MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744MediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1744MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
