# IKEA E2123

![IKEA E2123](<https://xaviml.github.io/controllerx/assets/controllers/E2123.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E2123`
- **Controller types:** [Media Player](<#media-player>) (`E2123MediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E2123>)

## Notes

The device supports other events which are not added to the default mapping. Please check [this GitHub issue](<https://github.com/xaviml/controllerx/issues/842>) for more information.

## Media Player

- **Class:** `E2123MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `toggle`, `play_pause` |  | `toggle`, `play_pause` | `play_pause` |
| `track_next` | `5002` | `step_0_1_0_0_0` | `next_track` |
| `track_previous` | `4002` | `step_1_1_0_0_0` | `previous_track` |
| `volume_up`, `volume_up_hold` |  | `move_with_on_off_0_255` | `click_volume_up` |
| `volume_down`, `volume_down_hold` |  | `move_with_on_off_1_255` | `click_volume_down` |
| `dots_1_initial_press` | `6000` | `2_initial_press_0` | `previous_source` |
| `dots_2_initial_press` | `7000` | `3_initial_press_0` | `next_source` |
|  | `1002` |  | `play` |
|  | `2001` | `move_0_255_0_0` | `hold_volume_up` |
|  | `2002`, `3002` |  | `release` |
|  | `3001` | `move_1_255_0_0` | `hold_volume_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: E2123MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2123MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2123MediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E2123MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
