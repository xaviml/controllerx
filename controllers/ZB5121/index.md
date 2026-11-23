# RGB Genie ZB5121

![RGB Genie ZB5121](<https://xaviml.github.io/controllerx/assets/controllers/ZB5121.jpeg>)

- **Manufacturer:** RGB Genie
- **Device ID:** `ZB5121`
- **Controller types:** [Light](<#light>) (`ZB5121LightController`)
- **Integrations:** [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ZB5121>)

## Light

- **Class:** `ZB5121LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"` | `on` |
| `"off"` | `off` |
| `step_with_on_off_0_32_0` | `click_brightness_up` |
| `move_with_on_off_0_50` | `hold_brightness_up` |
| `step_with_on_off_1_32_0` | `click_brightness_down` |
| `move_with_on_off_1_50` | `hold_brightness_down` |
| `recall_0_1` | *No action* |
| `stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: ZB5121LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
