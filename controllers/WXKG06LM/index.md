# Aqara WXKG06LM

![Aqara WXKG06LM](<https://xaviml.github.io/controllerx/assets/controllers/WXKG06LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG06LM`
- **Controller types:** [Light](<#light>) (`WXKG06LMLightController`), [Switch](<#switch>) (`WXKG06LMSwitchController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG06LM>)

## Notes

This controller supports the hold action, but not release. This means that there are no smooth brightness changes when holding, just step by step every time it is held.

## Light

- **Class:** `WXKG06LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `single` | `1002` | `toggle` |
| `double`, `hold` | `1004` | `click_brightness_up` |
|  | `1001` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG06LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG06LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG06LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

## Switch

- **Class:** `WXKG06LMSwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- | --- |
| `single` | `1002` | `toggle` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG06LMSwitchController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG06LMSwitchController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  switch: switch.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG06LMSwitchController
  integration: deconz
  controller: my_controller
  switch: switch.my_entity_id
```
