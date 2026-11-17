# Homematic HMSenMDIRWM55

![Homematic HMSenMDIRWM55](<https://xaviml.github.io/controllerx/assets/controllers/HMSenMDIRWM55.jpeg>)

- **Manufacturer:** Homematic
- **Device ID:** `HMSenMDIRWM55`
- **Controller types:** [Light](<#light>) (`HMSenMDIRWM55LightController`)
- **Integrations:** [Homematic](<https://xaviml.github.io/controllerx/start/integrations/homematic/index.md>) (`homematic`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=HMSenMDIRWM55>)

## Light

- **Class:** `HMSenMDIRWM55LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Homematic | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `PRESS_SHORT_1` | `off` |
| `PRESS_LONG_1` | `hold_brightness_down` |
| `PRESS_CONT_1`, `PRESS_CONT_2` | *No action* |
| `PRESS_LONG_RELEASE_1`, `PRESS_LONG_RELEASE_2` | `release` |
| `PRESS_SHORT_2` | `on` |
| `PRESS_LONG_2` | `hold_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: HMSenMDIRWM55LightController
  integration: homematic
  controller: my_controller
  light: light.my_entity_id
```
