# Philips HueSmartButton

![Philips HueSmartButton](<https://xaviml.github.io/controllerx/assets/controllers/HueSmartButton.jpeg>)

- **Manufacturer:** Philips
- **Device ID:** `HueSmartButton`
- **Controller types:** [Light](<#light>) (`HueSmartButtonLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`HueSmartButtonZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=HueSmartButton>)

## Light

- **Class:** `HueSmartButtonLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `"on"`, `"off"` | `1002` | `toggle` |
| `hold` | `1001` | `hold_brightness_toggle` |
| `release` | `1003` | `release` |
|  | `1000` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: HueSmartButtonLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: HueSmartButtonLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: HueSmartButtonLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `HueSmartButtonZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"`, `"off"` | `toggle` |
| `hold` | `hold_brightness_toggle` |
| `release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: HueSmartButtonZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: HueSmartButtonZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
