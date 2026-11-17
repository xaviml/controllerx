# OSRAM AC025XX00NJ

![OSRAM AC025XX00NJ](<https://xaviml.github.io/controllerx/assets/controllers/OsramAC025XX00NJ.jpeg>)

- **Manufacturer:** OSRAM
- **Device ID:** `OsramAC025XX00NJ`
- **Controller types:** [Light](<#light>) (`OsramAC025XX00NJLightController`)
- **Integrations:** [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=OsramAC025XX00NJ>)

## Notes

This controller is supported for AC0251100NJ / AC0251400NJ / AC0251600NJ / AC0251700NJ. The different models are just different colours.

## Light

- **Class:** `OsramAC025XX00NJLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `1002` | `1_on` | `on` |
| `1001` | `1_move_with_on_off` | `hold_brightness_up` |
| `1003`, `2003`, `3003` | `1_stop`, `3_move_hue`, `2_stop` | `release` |
| `2002` | `2_off` | `off` |
| `2001` | `2_move` | `hold_brightness_down` |
| `3002` | `3_move_to_color_temp` | `sync` |
| `3001` | `3_move_to_saturation` | `hold_color_up` |
|  | `3_move_to_level_with_on_off` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: OsramAC025XX00NJLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: OsramAC025XX00NJLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
