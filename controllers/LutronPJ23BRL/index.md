# Lutron PJ23BRL

![Lutron PJ23BRL](<https://xaviml.github.io/controllerx/assets/controllers/LutronPJ23BRL.jpeg>)

- **Manufacturer:** Lutron
- **Device ID:** `LutronPJ23BRL`
- **Controller types:** [Light](<#light>) (`LutronPJ23BRLLightController`), [Media Player](<#media-player>) (`LutronPJ23BRLMediaPlayerController`)
- **Integrations:** [State](<https://xaviml.github.io/controllerx/start/integrations/state/index.md>) (`state`), [Lutron Caseta](<https://xaviml.github.io/controllerx/start/integrations/lutron_caseta/index.md>) (`lutron_caseta`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=LutronPJ23BRL>)

## Notes

For the State integration, it requires the [LutronCasetaPro](<https://github.com/upsert/lutron-caseta-pro>) **custom** integration by upsert. **This will not work with the default Lutron Caseta integration.** All Lutron Caseta Pro Pico remotes supported by LutronCasetaPro are supported using this controller type, except for the 4-button PJ2-4B remotes, which have their own controller.

## Light

- **Class:** `LutronPJ23BRLLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| State | Lutron Caseta | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `1` | `button_2_press` | `on_full_brightness` |
| `8` | `button_5_press` | `hold_brightness_up` |
| `2` | `button_3_press` | `set_half_brightness` |
| `16` | `button_6_press` | `hold_brightness_down` |
| `4` | `button_4_press` | `off` |
| `0` | `button_5_release`, `button_6_release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: LutronPJ23BRLLightController
  integration: state
  controller: sensor.my_custom_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: LutronPJ23BRLLightController
  integration: lutron_caseta
  controller: 87654321
  light: light.my_entity_id
```

## Media Player

- **Class:** `LutronPJ23BRLMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| State | Lutron Caseta | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- | --- |
| `1` | `button_2_press` | `play_pause` |
| `8` | `button_5_press` | `hold_volume_up` |
| `2` | `button_3_press` | `next_source` |
| `16` | `button_6_press` | `hold_volume_down` |
| `4` | `button_4_press` | `next_track` |
| `0` | `button_5_release`, `button_6_release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: LutronPJ23BRLMediaPlayerController
  integration: state
  controller: sensor.my_custom_controller
  media_player: media_player.my_entity_id
```

```
example_app:
  module: controllerx
  class: LutronPJ23BRLMediaPlayerController
  integration: lutron_caseta
  controller: 87654321
  media_player: media_player.my_entity_id
```
