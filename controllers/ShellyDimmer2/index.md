# Shelly Dimmer2

![Shelly Dimmer2](<https://xaviml.github.io/controllerx/assets/controllers/ShellyDimmer2.jpeg>)

- **Manufacturer:** Shelly
- **Device ID:** `ShellyDimmer2`
- **Controller types:** [Light](<#light>) (`ShellyDimmer2LightController`)
- **Integrations:** [Shelly](<https://xaviml.github.io/controllerx/start/integrations/shelly/index.md>) (`shelly`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ShellyDimmer2>)

## Light

- **Class:** `ShellyDimmer2LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Shelly | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `single_1`, `long_1` | `toggle` |
| `single_2`, `long_2` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: ShellyDimmer2LightController
  integration: shelly
  controller: shellybutton-ABC123456
  light: light.my_entity_id
```
