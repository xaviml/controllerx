# Lutron PJ22BRL

![Lutron PJ22BRL](<https://xaviml.github.io/controllerx/assets/controllers/LutronPJ22BRL.jpeg>)

- **Manufacturer:** Lutron
- **Device ID:** `LutronPJ22BRL`
- **Controller types:** [Light](<#light>) (`LutronPJ22BRLLightController`), [Media Player](<#media-player>) (`LutronPJ22BRLMediaPlayerController`)
- **Integrations:** [State](<https://xaviml.github.io/controllerx/start/integrations/state/index.md>) (`state`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=LutronPJ22BRL>)

## Notes

For the State integration, it requires the [LutronCasetaPro](<https://github.com/upsert/lutron-caseta-pro>) **custom** integration by upsert. **This will not work with the default Lutron Caseta integration.** All Lutron Caseta Pro Pico remotes supported by LutronCasetaPro are supported using this controller type, except for the 4-button PJ2-4B remotes, which have their own controller.

## Light

- **Class:** `LutronPJ22BRLLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| State | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1` | `on_full_brightness` |
| `8` | `hold_brightness_up` |
| `16` | `hold_brightness_down` |
| `4` | `off` |
| `0` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: LutronPJ22BRLLightController
  integration: state
  controller: sensor.my_custom_controller
  light: light.my_entity_id
```

## Media Player

- **Class:** `LutronPJ22BRLMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| State | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- |
| `1` | `play_pause` |
| `8` | `hold_volume_up` |
| `16` | `hold_volume_down` |
| `4` | `next_track` |
| `0` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: LutronPJ22BRLMediaPlayerController
  integration: state
  controller: sensor.my_custom_controller
  media_player: media_player.my_entity_id
```
