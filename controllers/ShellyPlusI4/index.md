# Shelly PlusI4

![Shelly PlusI4](<https://xaviml.github.io/controllerx/assets/controllers/ShellyPlusI4.jpeg>)

- **Manufacturer:** Shelly
- **Device ID:** `ShellyPlusI4`
- **Controller types:** [Light](<#light>) (`ShellyPlusI4LightController`)
- **Integrations:** [Shelly](<https://xaviml.github.io/controllerx/start/integrations/shelly/index.md>) (`shelly`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ShellyPlusI4>)

## Light

- **Class:** `ShellyPlusI4LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Shelly | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `single_push_1` | `on` |
| `long_push_1` | `hold_color_up` |
| `btn_up_1`, `btn_up_2`, `btn_up_3`, `btn_up_4` | `release` |
| `double_push_1` | `on_full_color_temp` |
| `single_push_2` | `off` |
| `long_push_2` | `hold_color_down` |
| `double_push_2` | `on_min_color_temp` |
| `single_push_3` | `click_brightness_up` |
| `long_push_3` | `hold_brightness_up` |
| `double_push_3` | `on_full_brightness` |
| `single_push_4` | `click_brightness_down` |
| `long_push_4` | `hold_brightness_down` |
| `double_push_4` | `on_min_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: ShellyPlusI4LightController
  integration: shelly
  controller: shellybutton-ABC123456
  light: light.my_entity_id
```
