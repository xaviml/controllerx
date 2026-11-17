# Aqara WXKG11LMRemote

![Aqara WXKG11LMRemote](<https://xaviml.github.io/controllerx/assets/controllers/WXKG11LMRemote.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `WXKG11LMRemote`
- **Controller types:** [Light](<#light>) (`WXKG11LMRemoteLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`WXKG11LMRemoteZ2MLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=WXKG11LMRemote>)

## Light

- **Class:** `WXKG11LMRemoteLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `single` | `1002` | `single` | `toggle` |
| `double` | `1004` | `double` | `on_full_brightness` |
| `hold` | `1001` | `hold` | `hold_brightness_toggle` |
| `release` | `1003` | `release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG11LMRemoteLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG11LMRemoteLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG11LMRemoteLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG11LMRemoteLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `WXKG11LMRemoteZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `single` | `toggle` |
| `double` | `on_full_brightness` |
| `hold` | `hold_brightness_toggle` |
| `release` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: WXKG11LMRemoteZ2MLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: my_entity_id
```

```
example_app:
  module: controllerx
  class: WXKG11LMRemoteZ2MLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: my_entity_id
```
