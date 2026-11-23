# Aqara WXKG11LMSensorSwitch

![Aqara WXKG11LMSensorSwitch](<https://xaviml.github.io/controllerx/assets/controllers/WXKG11LMSensorSwitch.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG11LMSensorSwitch`
- **Controller types:** [Light](<#light>) (`WXKG11LMSensorSwitchLightController`)
- **Integrations:** [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG11LMSensorSwitch>)

## Light

- **Class:** `WXKG11LMSensorSwitchLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `1002` | `single` | `toggle` |
| `1004` | `double` | `on_full_brightness` |
| `1005` | `triple` | `on_min_brightness` |
| `1006` | `quadruple` | `set_half_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG11LMSensorSwitchLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG11LMSensorSwitchLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
