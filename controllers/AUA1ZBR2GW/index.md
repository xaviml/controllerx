# Aurora AUA1ZBR2GW

![Aurora AUA1ZBR2GW](<https://xaviml.github.io/controllerx/assets/controllers/AUA1ZBR2GW.jpeg>)

- **Manufacturer:** Aurora
- **Device ID:** `AUA1ZBR2GW`
- **Controller types:** [Light](<#light>) (`AUA1ZBR2GWLightController`)
- **Integrations:** [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=AUA1ZBR2GW>)

## Light

- **Class:** `AUA1ZBR2GWLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1_toggle`, `2_toggle` | `toggle` |
| `1_step_up`, `2_step_up` | `click_brightness_up` |
| `1_step_down`, `2_step_down` | `click_brightness_down` |
| `1_step_color_temp_up`, `2_step_color_temp_up` | `click_colortemp_up` |
| `1_step_color_temp_down`, `2_step_color_temp_down` | `click_colortemp_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: AUA1ZBR2GWLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
