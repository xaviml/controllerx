# Tuya TS0043

![Tuya TS0043](<https://xaviml.github.io/controllerx/assets/controllers/TS0043.jpeg>)

- **Manufacturer:** Tuya
- **Device ID:** `TS0043`
- **Controller types:** [Light](<#light>) (`TS0043LightController`), [Cover](<#cover>) (`TS0043CoverController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TS0043>)

## Light

- **Class:** `TS0043LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `1_single`, `2_single`, `3_single` | `1_remote_button_short_press`, `2_remote_button_short_press`, `3_remote_button_short_press` | `toggle` |
| `1_double`, `2_double`, `3_double` | `1_remote_button_double_press`, `2_remote_button_double_press`, `3_remote_button_double_press` | `click_brightness_up` |
| `1_hold`, `2_hold`, `3_hold` | `1_remote_button_long_press`, `2_remote_button_long_press`, `3_remote_button_long_press` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: TS0043LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: TS0043LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: TS0043LightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Cover

- **Class:** `TS0043CoverController`
- **Entity parameter:** `cover`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) |
| --- | --- |
| `1_single` | `open` |
| `2_single` | `stop` |
| `3_single` | `close` |

### Example configuration

```
example_app:
  module: controllerx
  class: TS0043CoverController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  cover: cover.my_entity_id
```

```
example_app:
  module: controllerx
  class: TS0043CoverController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  cover: cover.my_entity_id
```
