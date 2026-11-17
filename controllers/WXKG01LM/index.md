# Aqara WXKG01LM

![Aqara WXKG01LM](<https://xaviml.github.io/controllerx/assets/controllers/WXKG01LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG01LM`
- **Controller types:** [Light](<#light>) (`WXKG01LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXKG01LMZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG01LM>)

## Notes

The ZHA implementation of this button does not support hold and release actions yet.

## Light

- **Class:** `WXKG01LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `single` | `1002` | `single` | `toggle` |
| `double` | `1004` | `double` | `on_full_brightness` |
| `triple` | `1005` | `triple` | `on_min_brightness` |
| `quadruple` | `1006` | `quadruple` | `set_half_brightness` |
| `many` | `1010` |  | *No action* |
| `hold` | `1001` |  | `hold_brightness_toggle` |
| `release` | `1003` |  | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG01LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG01LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG01LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG01LMLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXKG01LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `single` | `toggle` |
| `double` | `on_full_brightness` |
| `triple` | `on_min_brightness` |
| `quadruple` | `set_half_brightness` |
| `many` | *No action* |
| `hold` | `hold_brightness_toggle` |
| `release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG01LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG01LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
