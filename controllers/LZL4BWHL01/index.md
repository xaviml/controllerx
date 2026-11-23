# Lutron LZL4BWHL01

![Lutron LZL4BWHL01](<https://xaviml.github.io/controllerx/assets/controllers/LZL4BWHL01.jpeg>)

- **Manufacturer:** Lutron
- **Device ID:** `LZL4BWHL01`
- **Controller types:** [Light](<#light>) (`LZL4BWHL01LightController`)
- **Integrations:** [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=LZL4BWHL01>)

## Light

- **Class:** `LZL4BWHL01LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `1002` | `move_to_level_with_on_off_254_4` | `on_full_brightness` |
| `2001` | `step_with_on_off_0_30_6` | `hold_brightness_up` |
| `2003`, `3003` | `stop` | `release` |
| `3001` | `step_1_30_6` | `hold_brightness_down` |
| `4002` | `move_to_level_with_on_off_0_4` | `off` |

### Example configuration

```
example_app:
  module: controllerx
  class: LZL4BWHL01LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: LZL4BWHL01LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
