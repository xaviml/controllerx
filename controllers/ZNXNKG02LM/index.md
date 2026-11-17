# Aqara ZNXNKG02LM

![Aqara ZNXNKG02LM](<https://xaviml.github.io/controllerx/assets/controllers/ZNXNKG02LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `ZNXNKG02LM`
- **Controller types:** [Light](<#light>) (`ZNXNKG02LMLightController`), [Media Player](<#media-player>) (`ZNXNKG02LMMediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ZNXNKG02LM>)

## Light

- **Class:** `ZNXNKG02LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `single` | `toggle` |
| `double` | `on_full_brightness` |
| `hold` | `hold_color_toggle` |
| `release`, `stop_rotating` | `release` |
| `start_rotating` | `brightness_from_controller_angle` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZNXNKG02LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ZNXNKG02LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Media Player

- **Class:** `ZNXNKG02LMMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- |
| `single` | `play_pause` |
| `double` | `next_track` |
| `hold` | `previous_track` |
| `release`, `stop_rotating` | `release` |
| `start_rotating` | `volume_from_controller_angle` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZNXNKG02LMMediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: ZNXNKG02LMMediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```
