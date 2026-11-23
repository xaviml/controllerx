# Smartkontakten SK5700002228949

![Smartkontakten SK5700002228949](<https://xaviml.github.io/controllerx/assets/controllers/SK5700002228949.jpeg>)

- **Manufacturer:** Smartkontakten
- **Device ID:** `SK5700002228949`
- **Controller types:** [Light](<#light>) (`SK5700002228949LightController`)
- **Integrations:** [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=SK5700002228949>)

## Light

- **Class:** `SK5700002228949LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1002` | `on` |
| `1001` | `hold_brightness_up` |
| `1003`, `3003`, `2003`, `4003` | `release` |
| `3002` | `off` |
| `3001` | `hold_brightness_down` |
| `2002` | `click_color_up` |
| `2001` | `hold_color_up` |
| `4002` | `click_color_down` |
| `4001` | `hold_color_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: SK5700002228949LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```
