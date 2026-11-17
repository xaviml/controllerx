# Tuya TS0042

![Tuya TS0042](<https://xaviml.github.io/controllerx/assets/controllers/TS0042.jpeg>)

- **Manufacturer:** Tuya
- **Device ID:** `TS0042`
- **Controller types:** [Light](<#light>) (`TS0042LightController`)
- **Integrations:** [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TS0042>)

## Light

- **Class:** `TS0042LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1_remote_button_short_press` | `on` |
| `1_remote_button_double_press` | `click_brightness_up` |
| `1_remote_button_long_press` | `on_full_brightness` |
| `2_remote_button_short_press` | `off` |
| `2_remote_button_double_press` | `on_min_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: TS0042LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
