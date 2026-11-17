# Homematic HMPBI4FM

![Homematic HMPBI4FM](<https://xaviml.github.io/controllerx/assets/controllers/HMPBI4FM.jpeg>)

- **Manufacturer:** Homematic
- **Device ID:** `HMPBI4FM`
- **Controller types:** [Light](<#light>) (`HMPBI4FMLightController`)
- **Integrations:** [Homematic](<https://xaviml.github.io/controllerx/start/integrations/homematic/index.md>) (`homematic`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=HMPBI4FM>)

## Light

- **Class:** `HMPBI4FMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Homematic | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `PRESS_SHORT_1` | `off` |
| `PRESS_CONT_1`, `PRESS_CONT_2`, `PRESS_CONT_3`, `PRESS_CONT_4` | *No action* |
| `PRESS_LONG_1` | `click_color_down` |
| `PRESS_SHORT_2` | `on` |
| `PRESS_LONG_2` | `click_color_up` |
| `PRESS_SHORT_3` | `click_brightness_down` |
| `PRESS_LONG_3` | `on_min_brightness` |
| `PRESS_SHORT_4` | `click_brightness_up` |
| `PRESS_LONG_4` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: HMPBI4FMLightController
  integration: homematic
  controller: my_controller
  light: light.my_entity_id
```
