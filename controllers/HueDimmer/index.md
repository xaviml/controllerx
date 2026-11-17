# Philips HueDimmer

![Philips HueDimmer](<https://xaviml.github.io/controllerx/assets/controllers/HueDimmer.jpeg>)

- **Manufacturer:** Philips
- **Device ID:** `HueDimmer`
- **Controller types:** [Light](<#light>) (`HueDimmerController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`HueDimmerZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=HueDimmer>)

## Notes

When using **z2m**, the device needs to be flagged as `legacy: false`, as the [Zigbee2MQTT documentation recommends](<https://www.zigbee2mqtt.io/devices/324131092621.html#options>).

When using **z2m** and the multiple clicks functionality, make sure to remove the `multiple_press_timeout` option from the device-specific configuration (`devices.yaml`).

When using **deCONZ**, all the click actions are mapped to the X002 actions, which are fired when the button is released after being clicked.

## Light

- **Class:** `HueDimmerController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `on_press_release` | `1002` | `on_short_release` | `on` |
| `on_hold` | `1001` | `on_hold` | `hold_color_up` |
| `on_hold_release`, `up_hold_release`, `down_hold_release`, `off_hold_release` | `1003`, `2003`, `3003`, `4003` | `off_long_release`, `down_long_release`, `up_long_release`, `on_long_release` | `release` |
| `up_press_release` | `2002` | `up_short_release` | `click_brightness_up` |
| `up_hold` | `2001` | `up_hold` | `hold_brightness_up` |
| `down_press_release` | `3002` | `down_short_release` | `click_brightness_down` |
| `down_hold` | `3001` | `down_hold` | `hold_brightness_down` |
| `off_press_release` | `4002` | `off_short_release` | `off` |
| `off_hold` | `4001` | `off_hold` | `hold_color_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: HueDimmerController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: HueDimmerController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: HueDimmerController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: HueDimmerController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `HueDimmerZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `on_press_release` | `on` |
| `on_hold` | `hold_colortemp_up` |
| `on_hold_release`, `up_hold_release`, `down_hold_release`, `off_hold_release` | `release` |
| `up_press_release` | `click_brightness_up` |
| `up_hold` | `hold_brightness_up` |
| `down_press_release` | `click_brightness_down` |
| `down_hold` | `hold_brightness_down` |
| `off_press_release` | `off` |
| `off_hold` | `hold_colortemp_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: HueDimmerZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: HueDimmerZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
