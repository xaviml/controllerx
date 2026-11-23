# RGB Genie ZB5122

![RGB Genie ZB5122](<https://xaviml.github.io/controllerx/assets/controllers/ZB5122.jpeg>)

- **Manufacturer:** RGB Genie
- **Device ID:** `ZB5122`
- **Controller types:** [Light](<#light>) (`ZB5122LightController`)
- **Integrations:** [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ZB5122>)

## Light

- **Class:** `ZB5122LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `hold_brightness_up` | `hold_brightness_up` |
| `hold_brightness_down` | `hold_brightness_down` |
| `stop`, `stop_move_hue`, `stop_move_step` | `release` |
| `move_to_color` | `click_xycolor_up` |
| `move_hue` | `hold_xycolor_up` |
| `move_to_color_temp` | `colortemp_from_controller` |
| `move_color_temp` | `hold_colortemp_toggle` |
| `recall_0_1` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: ZB5122LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
