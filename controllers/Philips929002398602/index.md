# Philips 929002398602

![Philips 929002398602](<https://xaviml.github.io/controllerx/assets/controllers/Philips929002398602.jpeg>)

- **Manufacturer:** Philips
- **Device ID:** `Philips929002398602`
- **Controller types:** [Light](<#light>) (`Philips929002398602LightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`Philips929002398602Z2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=Philips929002398602>)

## Light

- **Class:** `Philips929002398602LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `on_press_release`, `on_hold` | `1002`, `1001` | `on_hold`, `on_short_release` | `toggle` |
| `on_hold_release`, `up_hold_release`, `down_hold_release`, `off_hold_release` | `1003`, `2003`, `3003`, `4003` | `off_long_release`, `down_long_release`, `up_long_release`, `on_long_release` | `release` |
| `up_press_release` | `2002` | `up_short_release` | `click_brightness_up` |
| `up_hold` | `2001` | `up_hold` | `hold_brightness_up` |
| `down_press_release` | `3002` | `down_short_release` | `click_brightness_down` |
| `down_hold` | `3001` | `down_hold` | `hold_brightness_down` |
| `off_press_release` | `4002` | `off_short_release` | `click_color_up` |
| `off_hold` | `4001` | `off_hold` | `hold_color_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: Philips929002398602LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929002398602LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929002398602LightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929002398602LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `Philips929002398602Z2MLightController`
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
  class: Philips929002398602Z2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: Philips929002398602Z2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
