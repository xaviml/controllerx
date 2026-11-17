# Lutron PJ24B

![Lutron PJ24B](<https://xaviml.github.io/controllerx/assets/controllers/LutronPJ24B.jpeg>)

- **Manufacturer:** Lutron
- **Device ID:** `LutronPJ24B`
- **Controller types:** [Light](<#light>) (`LutronPJ24BLightController`), [Media Player](<#media-player>) (`LutronPJ24BMediaPlayerController`)
- **Integrations:** [State](<https://xaviml.github.io/controllerx/start/integrations/state/index.md>) (`state`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=LutronPJ24B>)

## Notes

For the State integration, it requires the [LutronCasetaPro](<https://github.com/upsert/lutron-caseta-pro>) **custom** integration by upsert. **This will not work with the default Lutron Caseta integration.**

## Light

- **Class:** `LutronPJ24BLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| State | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1` | `on_full_brightness` |
| `2` | `hold_brightness_up` |
| `4` | `hold_brightness_down` |
| `8` | `off` |
| `0` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: LutronPJ24BLightController
  integration: state
  controller: sensor.my_custom_controller
  light: light.my_entity_id
```

## Media Player

- **Class:** `LutronPJ24BMediaPlayerController`
- **Entity parameter:** `media_player`
- **Default delay:** `500ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| State | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#media-player>) |
| --- | --- |
| `1` | `play_pause` |
| `2` | `hold_volume_up` |
| `4` | `hold_volume_down` |
| `8` | `next_track` |
| `0` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: LutronPJ24BMediaPlayerController
  integration: state
  controller: sensor.my_custom_controller
  media_player: media_player.my_entity_id
```
