# Aqara WXKG02LM

![Aqara WXKG02LM](<https://xaviml.github.io/controllerx/assets/controllers/WXKG02LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG02LM`
- **Controller types:** [Light](<#light>) (`WXKG02LMLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXKG02LMZ2MLightController`), [Switch](<#switch>) (`WXKG02LMSwitchController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG02LM>)

## Notes

Note that all actions related to both left and right do the same. This is because ControllerX is designed to control just one entity (light or media player). So, you can include the `actions` parameter to include the actions needed. You can check [here](<https://github.com/xaviml/controllerx/issues/18#issuecomment-582535634>) for reference.

Also, this controller supports the hold action, but not release. This means that there are no smooth brightness changes when holding, just step by step every time it is held.

## Light

- **Class:** `WXKG02LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `single_both`, `single_left`, `single_right` | `1002`, `2002`, `3002` | `both_single`, `left_single`, `right_single` | `toggle` |
| `double_both`, `double_left`, `double_right` | `1004`, `2004`, `3004` | `both_double`, `left_double`, `right_double` | `click_brightness_up` |
| `hold_both`, `hold_left`, `hold_right` | `1001`, `2001`, `3001` | `both_long press`, `left_long press`, `right_long press` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG02LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXKG02LMZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `single_both`, `single_left`, `single_right` | `toggle` |
| `double_both`, `double_left`, `double_right` | `click_brightness_up` |
| `hold_both`, `hold_left`, `hold_right` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG02LMZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```

## Switch

- **Class:** `WXKG02LMSwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- | --- | --- |
| `single_both`, `single_left`, `single_right` | `1002`, `2002`, `3002` | `both_single`, `left_single`, `right_single` | `toggle` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG02LMSwitchController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMSwitchController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMSwitchController
  integration: deconz
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG02LMSwitchController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  switch: switch.my_entity_id
```
