# Philips 929003017102

![Philips 929003017102](<https://xaviml.github.io/controllerx/assets/controllers/Philips929003017102.jpeg>)

- **Manufacturer:** Philips
- **Device ID:** `Philips929003017102`
- **Controller types:** [Light](<#light>) (`Philips929003017102LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`Philips929003017102Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=Philips929003017102>)

## Notes

This controller has 4 modes, and depending on which one is used, it will trigger one action or another: single\_rocker, single\_push\_button, dual\_rocker, dual\_push\_button. You can read more about it in these threads: [deCONZ](<https://github.com/dresden-elektronik/deconz-rest-plugin/issues/4566>) and [Zigbee2MQTT](<https://github.com/Koenkk/zigbee-herdsman-converters/issues/2393>).

## Light

- **Class:** `Philips929003017102LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `left_press_release`, `right_press_release` | `1002`, `2002` | `left_press_release`, `right_short_release` | `toggle` |
| `left_hold`, `right_hold` | `1001`, `2001` | `left_hold`, `right_hold` | `hold_brightness_toggle` |
| `left_hold_release`, `right_hold_release` | `1003`, `2003` | `left_hold_release`, `right_long_release` | `release` |
|  | `1000`, `2000` |  | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: Philips929003017102LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929003017102LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929003017102LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929003017102LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `Philips929003017102Z2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `left_press_release`, `right_press_release` | `toggle` |
| `left_hold`, `right_hold` | `hold_brightness_toggle` |
| `left_hold_release`, `right_hold_release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: Philips929003017102Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929003017102Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
