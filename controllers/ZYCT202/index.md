# Trust ZYCT202

![Trust ZYCT202](<https://xaviml.github.io/controllerx/assets/controllers/ZYCT202.jpeg>)

- **Manufacturer:** Trust
- **Device ID:** `ZYCT202`
- **Controller types:** [Light](<#light>) (`ZYCT202LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`ZYCT202Z2MLightController`), [Media Player](<#media-player>) (`ZYCT202MediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ZYCT202>)

## Light

- **Class:** `ZYCT202LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"` | `on` |
| `up-press` | `hold_brightness_up` |
| `down-press` | `hold_brightness_down` |
| `"off"` | `off` |
| `stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZYCT202LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ZYCT202LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `ZYCT202Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `up-press` | `hold_brightness_up` |
| `down-press` | `hold_brightness_down` |
| `"off"` | `off` |
| `stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZYCT202Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: ZYCT202Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `ZYCT202MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- |
| `"on"`, `"off"` | `play_pause` |
| `up-press` | `hold_volume_up` |
| `down-press` | `hold_volume_down` |
| `stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZYCT202MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: ZYCT202MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```
