# Homematic HMPB6WM55

![Homematic HMPB6WM55](<https://xaviml.github.io/controllerx/assets/controllers/HMPB6WM55.jpeg>)

- **Manufacturer:** Homematic
- **Device ID:** `HMPB6WM55`
- **Controller types:** [Light](<#light>) (`HMPB6WM55LightController`)
- **Integrations:** [Homematic](<https://xaviml.github.io/controllerx/start/integrations/homematic/index.md>) (`homematic`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=HMPB6WM55>)

## Light

- **Class:** `HMPB6WM55LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Homematic | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `PRESS_SHORT_1` | `off` |
| `PRESS_CONT_1`, `PRESS_CONT_2`, `PRESS_CONT_3`, `PRESS_CONT_4`, `PRESS_CONT_5`, `PRESS_CONT_6` | *No action* |
| `PRESS_LONG_1`, `PRESS_LONG_2` | `sync` |
| `PRESS_LONG_RELEASE_1`, `PRESS_LONG_RELEASE_2`, `PRESS_LONG_RELEASE_3`, `PRESS_LONG_RELEASE_4`, `PRESS_LONG_RELEASE_5`, `PRESS_LONG_RELEASE_6` | `release` |
| `PRESS_SHORT_2` | `on` |
| `PRESS_SHORT_3` | `click_brightness_down` |
| `PRESS_LONG_3` | `hold_brightness_down` |
| `PRESS_SHORT_4` | `click_brightness_up` |
| `PRESS_LONG_4` | `hold_brightness_up` |
| `PRESS_SHORT_5` | `click_color_down` |
| `PRESS_LONG_5` | `hold_color_down` |
| `PRESS_SHORT_6` | `click_color_up` |
| `PRESS_LONG_6` | `hold_color_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: HMPB6WM55LightController
  integration: homematic
  controller: my_controller
  light: light.my_entity_id
```
