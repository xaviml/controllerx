# Shelly I3

![Shelly I3](<https://xaviml.github.io/controllerx/assets/controllers/ShellyI3.jpeg>)

- **Manufacturer:** Shelly
- **Device ID:** `ShellyI3`
- **Controller types:** [Light](<#light>) (`ShellyI3LightController`)
- **Integrations:** [ShellyForHass](<https://xaviml.github.io/controllerx/start/integrations/shellyforhass/index.md>) (`shellyforhass`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ShellyI3>)

## Light

- **Class:** `ShellyI3LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| ShellyForHass | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `single` | `click_brightness_up` |
| `long` | `click_brightness_down` |
| `double` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: ShellyI3LightController
  integration: shellyforhass
  controller: binary_sensor.shelly_button_switch
  light: light.my_entity_id
```
