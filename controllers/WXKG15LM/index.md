# Aqara WXKG15LM

![Aqara WXKG15LM](<https://xaviml.github.io/controllerx/assets/controllers/WXKG15LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG15LM`
- **Controller types:** [Light](<#light>) (`WXKG15LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXKG15LMZ2MLightController`), [Switch](<#switch>) (`WXKG15LMSwitchController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG15LM>)

## Light

- **Class:** `WXKG15LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `single_both`, `single_left`, `single_right` | `toggle` |
| `double_both`, `double_left`, `double_right` | `click_brightness_up` |
| `triple_both`, `triple_left`, `triple_right` | `click_brightness_down` |
| `hold_both`, `hold_left`, `hold_right` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG15LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG15LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXKG15LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `single_both`, `single_left`, `single_right` | `toggle` |
| `double_both`, `double_left`, `double_right` | `click_brightness_up` |
| `triple_both`, `triple_left`, `triple_right` | `click_brightness_down` |
| `hold_both`, `hold_left`, `hold_right` | `on_full_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG15LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG15LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Switch

- **Class:** `WXKG15LMSwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- |
| `single_both`, `single_left`, `single_right` | `toggle` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG15LMSwitchController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG15LMSwitchController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  switch: switch.my_entity_id
```
