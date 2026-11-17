# Aqara MFKZQ01LM

![Aqara MFKZQ01LM](<https://xaviml.github.io/controllerx/assets/controllers/MFKZQ01LM.jpeg>)

- **Manufacturer:** Aqara
- **Device ID:** `MFKZQ01LM`
- **Controller types:** [Light](<#light>) (`MFKZQ01LMLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`), [ZHA](<https://xaviml.github.io/controllerx/start/integrations/zha/index.md>) (`zha`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=MFKZQ01LM>)

## Notes

This controller does not have a self-explanatory way to be used, since its main purpose is to be customized. This is why we recommend customizing it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

The deCONZ integration should be added with [type gesture](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>).

## Light

- **Class:** `MFKZQ01LMLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | ZHA | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- | --- |
| `shake` | `1` | `shake` | `on_min_brightness` |
| `tap` | `6` | `knock` | `toggle` |
| `slide` | `5` | `slide` | `on_full_brightness` |
| `flip180` | `4` | `flip180` | `click_color_up` |
| `flip90` | `3` | `flip90` | `click_color_down` |
| `rotate_left` | `8` | `rotate_left` | `click_brightness_down` |
| `rotate_right` | `7` | `rotate_right` | `click_brightness_up` |

### Example configuration

```
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  integration: zha
  controller: 00:11:22:33:44:55:66:77:88
  light: light.my_entity_id
```
