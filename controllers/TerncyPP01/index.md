# Terncy PP01

![Terncy PP01](<https://xaviml.github.io/controllerx/assets/controllers/TerncyPP01.jpeg>)

- **Manufacturer:** Terncy
- **Device ID:** `TerncyPP01`
- **Controller types:** [Light](<#light>) (`TerncyPP01LightController`)
- **Integrations:** [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TerncyPP01>)

## Light

- **Class:** `TerncyPP01LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `button_single` | `toggle` |
| `button_double` | `on_full_brightness` |
| `button_triple` | `on_min_brightness` |
| `button_quadruple` | `set_half_brightness` |
| `button_quintuple` | `set_half_color_temp` |

### Example configuration

```
example_app:
  module: controllerx
  class: TerncyPP01LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
