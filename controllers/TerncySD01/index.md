# Terncy SD01

![Terncy SD01](<https://xaviml.github.io/controllerx/assets/controllers/TerncySD01.jpeg>)

- **Manufacturer:** Terncy
- **Device ID:** `TerncySD01`
- **Controller types:** [Light](<#light>) (`TerncySD01LightController`), [Media Player](<#media-player>) (`TerncySD01MediaPlayerController`)
- **Integrations:** [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TerncySD01>)

## Light

- **Class:** `TerncySD01LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `button_single` | `toggle` |
| `button_double` | `on_full_brightness` |
| `button_triple` | `on_min_brightness` |
| `button_quadruple` | `set_half_brightness` |
| `button_quintuple` | `set_half_color_temp` |
| `rotate_left` | `click_brightness_down` |
| `rotate_right` | `click_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: TerncySD01LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Media Player

- **Class:** `TerncySD01MediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- |
| `button_single` | `play_pause` |
| `button_double` | `mute` |
| `button_triple` | `next_track` |
| `button_quadruple` | `previous_track` |
| `button_quintuple` | `next_source` |
| `rotate_left` | `click_volume_down` |
| `rotate_right` | `click_volume_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: TerncySD01MediaPlayerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  media_player: media_player.my_entity_id
```
