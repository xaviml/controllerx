# SmartThings Button

![SmartThings Button](<https://xaviml.github.io/controllerx/assets/controllers/SmartThingsButton.jpeg>)

- **Manufacturer:** SmartThings
- **Device ID:** `SmartThingsButton`
- **Controller types:** [Light](<#light>) (`SmartThingsButtonLightController`), [Media Player](<#media-player>) (`SmartThingsButtonMediaPlayerController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=SmartThingsButton>)

## Light

- **Class:** `SmartThingsButtonLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `single` | `1002` | `button_single_1_0_0_0` | `toggle` |
| `double` | `1004` | `button_double_2_0_0_0` | `on_full_brightness` |
| `hold` | `1001` | `button_hold_3_0_0_0` | `set_half_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: SmartThingsButtonLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: SmartThingsButtonLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: SmartThingsButtonLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: SmartThingsButtonLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Media Player

- **Class:** `SmartThingsButtonMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- | --- |
| `single_click` | `1002` | `button_single_1_0_0_0` | `play_pause` |
| `double_click` | `1004` | `button_double_2_0_0_0` | `next_track` |
| `hold` | `1001` | `button_hold_3_0_0_0` | `previous_track` |

### Example configuration

```
example_app:
  module: controllerx
  class: SmartThingsButtonMediaPlayerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: SmartThingsButtonMediaPlayerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: SmartThingsButtonMediaPlayerController
  integration: deconz
  controller: my_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: SmartThingsButtonMediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
