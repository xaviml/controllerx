# IKEA E1743

![IKEA E1743](<https://xaviml.github.io/controllerx/assets/controllers/E1743.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E1743`
- **Controller types:** [Light](<#light>) (`E1743Controller`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E1743Z2MLightController`), [Media Player](<#media-player>) (`E1743MediaPlayerController`), [Switch](<#switch>) (`E1743SwitchController`), [Cover](<#cover>) (`E1743CoverController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E1743>)

## Light

- **Class:** `E1743Controller`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `on` |
| `"off"` | `2002` | `"off"` | `off` |
| `brightness_move_up` | `1001` | `move_with_on_off_0_83` | `hold_brightness_up` |
| `brightness_move_down` | `2001` | `move_1_83_0_0` | `hold_brightness_down` |
| `brightness_stop` | `1003`, `2003` | `stop`, `stop_with_on_off` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1743Controller
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743Controller
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743Controller
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743Controller
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E1743Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1743Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Media Player

- **Class:** `E1743MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `play_pause` |
| `"off"` | `2002` | `"off"` | `next_track` |
| `brightness_move_up` | `1001` | `move_with_on_off_0_83` | `hold_volume_up` |
| `brightness_move_down` | `2001` | `move_1_83_0_0` | `hold_volume_down` |
| `brightness_stop` | `1003`, `2003` | `stop`, `stop_with_on_off` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1743MediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743MediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743MediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```

## Switch

- **Class:** `E1743SwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `on` |
| `"off"` | `2002` | `"off"` | `off` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1743SwitchController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743SwitchController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743SwitchController
  integration: deconz
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743SwitchController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  switch: switch.my_entity_id
```

## Cover

- **Class:** `E1743CoverController`
- **Entity parameter:** `cover`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `toggle_open` |
| `"off"` | `2002` | `"off"` | `toggle_close` |
| `brightness_move_up` | `1001` | `move_with_on_off_0_83` | `open` |
| `brightness_move_down` | `2001` | `move_1_83_0_0` | `close` |
| `brightness_stop` | `1003`, `2003` | `stop`, `stop_with_on_off` | `stop` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1743CoverController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743CoverController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743CoverController
  integration: deconz
  controller: my_controller
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1743CoverController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  cover: cover.my_entity_id
```
