# Lutron Z31BRL

![Lutron Z31BRL](<https://xaviml.github.io/controllerx/assets/controllers/Z31BRL.jpeg>)

- **Manufacturer:** Lutron
- **Device ID:** `Z31BRL`
- **Controller types:** [Light](<#light>) (`Z31BRLLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`Z31BRLZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=Z31BRL>)

## Light

- **Class:** `Z31BRLLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `brightness_move_to_level` |  | `brightness_from_controller_level` |
|  | `1002` | `toggle` |
|  | `2002` | `click_brightness_up` |
|  | `3002` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: Z31BRLLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Z31BRLLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Z31BRLLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `Z31BRLZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `brightness_move_to_level` | `brightness_from_controller_level` |

### Example configuration

```
example_app:
  module: controllerx
  class: Z31BRLZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: Z31BRLZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
