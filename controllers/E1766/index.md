# IKEA E1766

![IKEA E1766](<https://xaviml.github.io/controllerx/assets/controllers/E1766.jpeg>)

- **Manufacturer:** IKEA
- **Device ID:** `E1766`
- **Controller types:** [Light](<#light>) (`E1766LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`E1766Z2MLightController`), [Switch](<#switch>) (`E1766SwitchController`), [Cover](<#cover>) (`E1766CoverController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=E1766>)

## Light

- **Class:** `E1766LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `open` | `1002` | `up_open` | `on` |
| `close` | `2002` | `down_close` | `off` |
|  | `1003` |  | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1766LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `E1766Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `open` | `on` |
| `close` | `off` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1766Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Switch

- **Class:** `E1766SwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- | --- | --- |
| `open` | `1002` | `up_open` | `on` |
| `close` | `2002` | `down_close` | `off` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1766SwitchController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766SwitchController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766SwitchController
  integration: deconz
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766SwitchController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  switch: switch.my_entity_id
```

## Cover

- **Class:** `E1766CoverController`
- **Entity parameter:** `cover`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) |
| --- | --- | --- | --- |
| `open` | `1002` | `up_open` | `toggle_open` |
| `close` | `2002` | `down_close` | `toggle_close` |
| `stop` | `1003`, `2003` | `stop` | `stop` |

### Example configuration

```
example_app:
  module: controllerx
  class: E1766CoverController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766CoverController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766CoverController
  integration: deconz
  controller: my_controller
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: E1766CoverController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  cover: cover.my_entity_id
```
