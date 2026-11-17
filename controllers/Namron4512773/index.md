# Namron 4512773

![Namron 4512773](<https://xaviml.github.io/controllerx/assets/controllers/Namron4512773.jpeg>)

- **Manufacturer:** Namron
- **Device ID:** `Namron4512773`
- **Controller types:** [Light](<#light>) (`Namron4512773LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`Namron4512773Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=Namron4512773>)

## Notes

The Namron 4512773 has four groups, and with swappable physical buttons it is intended to control one, two, or four buttons. To make this work with ControllerX, you can use one app per light you want to control.

## Light

- **Class:** `Namron4512773LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `on_l1`, `on_l2`, `on_l3`, `on_l4` | `on` |
| `off_l1`, `off_l2`, `off_l3`, `off_l4` | `off` |
| `brightness_move_up_l1`, `brightness_move_up_l2`, `brightness_move_up_l3`, `brightness_move_up_l4` | `hold_brightness_up` |
| `brightness_move_down_l1`, `brightness_move_down_l2`, `brightness_move_down_l3`, `brightness_move_down_l4` | `hold_brightness_down` |
| `brightness_stop_l1`, `brightness_stop_l2`, `brightness_stop_l3`, `brightness_stop_l4` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: Namron4512773LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Namron4512773LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `Namron4512773Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `on_l1`, `on_l2`, `on_l3`, `on_l4` | `on` |
| `off_l1`, `off_l2`, `off_l3`, `off_l4` | `off` |
| `brightness_move_up_l1`, `brightness_move_up_l2`, `brightness_move_up_l3`, `brightness_move_up_l4` | `hold_brightness_up` |
| `brightness_move_down_l1`, `brightness_move_down_l2`, `brightness_move_down_l3`, `brightness_move_down_l4` | `hold_brightness_down` |
| `brightness_stop_l1`, `brightness_stop_l2`, `brightness_stop_l3`, `brightness_stop_l4` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: Namron4512773Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: Namron4512773Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
