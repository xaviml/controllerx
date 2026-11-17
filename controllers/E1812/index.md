# IKEA E1812

![IKEA E1812](<https://xaviml.github.io/controllerx/assets/controllers/E1812.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E1812`
- **Controller types:** [Light](<#light>) (`E1812LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E1812Z2MLightController`), [Switch](<#switch>) (`E1812SwitchController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E1812>)

## Light

- **Class:** `E1812LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `toggle` |
| `brightness_move_up` | `1001` | `move_with_on_off` | `hold_brightness_toggle` |
| `brightness_stop` | `1003` | `stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1812LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E1812Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"` | `toggle` |
| `brightness_move_up` | `hold_brightness_toggle` |
| `brightness_stop` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1812Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Switch

- **Class:** `E1812SwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- | --- | --- |
| `"on"` | `1002` | `"on"` | `toggle` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1812SwitchController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812SwitchController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812SwitchController
  integration: deconz
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1812SwitchController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  switch: switch.my_entity_id
```
