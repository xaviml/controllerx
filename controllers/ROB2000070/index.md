# ROBB ROB2000070

![ROBB ROB2000070](<https://xaviml.github.io/controllerx/assets/controllers/ROB2000070.jpeg>)

- **Manufacturer:** ROBB
- **Device ID:** `ROB2000070`
- **Controller types:** [Light](<#light>) (`ROB2000070LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`ROB2000070Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=ROB2000070>)

## Notes

Note that each button performs the same actions. This is because ControllerX is designed to control just one entity (light or media player). So, you can include the `actions` parameter to include the actions needed, or use the `mapping` attribute to define a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>). You can check [here](<https://github.com/xaviml/controllerx/issues/18#issuecomment-582535634>) for reference.

This controller is a white-label version of the Sunricher SR-ZG9001K8-DIM.

## Light

- **Class:** `ROB2000070LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `on_1`, `on_2`, `on_3`, `on_4` | `on` |
| `off_1`, `off_2`, `off_3`, `off_4` | `off` |
| `brightness_move_up_1`, `brightness_move_up_2`, `brightness_move_up_3`, `brightness_move_up_4` | `hold_brightness_up` |
| `brightness_move_down_1`, `brightness_move_down_2`, `brightness_move_down_3`, `brightness_move_down_4` | `hold_brightness_down` |
| `brightness_stop_1`, `brightness_stop_2`, `brightness_stop_3`, `brightness_stop_4` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: ROB2000070LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: ROB2000070LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `ROB2000070Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `on_1`, `on_2`, `on_3`, `on_4` | `on` |
| `off_1`, `off_2`, `off_3`, `off_4` | `off` |
| `brightness_move_up_1`, `brightness_move_up_2`, `brightness_move_up_3`, `brightness_move_up_4` | `hold_brightness_up` |
| `brightness_move_down_1`, `brightness_move_down_2`, `brightness_move_down_3`, `brightness_move_down_4` | `hold_brightness_down` |
| `brightness_stop_1`, `brightness_stop_2`, `brightness_stop_3`, `brightness_stop_4` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: ROB2000070Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: ROB2000070Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
