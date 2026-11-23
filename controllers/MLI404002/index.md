# Müller Licht MLI404002

![Müller Licht MLI404002](<https://xaviml.github.io/controllerx/assets/controllers/MLI404002.jpeg>)

- **Manufacturer:** Müller Licht
- **Device ID:** `MLI404002`
- **Controller types:** [Light](<#light>) (`MLI404002LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`MLI404002Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=MLI404002>)

## Light

- **Class:** `MLI404002LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `"on"`, `"off"` | `"on"`, `"off"` | `toggle` |
| `brightness_step_up` | `step_up` | `click_brightness_up` |
| `brightness_step_down` | `step_down` | `click_brightness_down` |
| `brightness_move_up` | `move_up` | `hold_brightness_up` |
| `brightness_move_down` | `move_down` | `hold_brightness_down` |
| `brightness_stop` | `stop` | `release` |
| `recall_1` | `recall` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: MLI404002LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MLI404002LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MLI404002LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `MLI404002Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `"on"`, `"off"` | `toggle` |
| `brightness_step_up` | `click_brightness_up` |
| `brightness_step_down` | `click_brightness_down` |
| `brightness_move_up` | `hold_brightness_up` |
| `brightness_move_down` | `hold_brightness_down` |
| `brightness_stop` | `release` |
| `recall_1` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: MLI404002Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: MLI404002Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
