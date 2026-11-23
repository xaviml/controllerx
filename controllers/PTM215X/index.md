# Philips PTM215X

![Philips PTM215X](<https://xaviml.github.io/controllerx/assets/controllers/PTM215X.jpeg>)

- **Manufacturer:** Philips
- **Device ID:** `PTM215X`
- **Controller types:** [Light](<#light>) (`PTM215XLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`), [deCONZ](<https://xaviml.github.io/controllerx/start/integrations/deconz/index.md>) (`deconz`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=PTM215X>)

## Notes

Check the button mapping [here](<https://phoscon.de/en/support#pairing-friends-of-hue-switch>).

## Light

- **Class:** `PTM215XLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | deCONZ | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- | --- |
| `press_1` | `1002` | `on` |
| `release_1`, `release_2`, `release_3`, `release_4`, `release_1_and_3`, `release_2_and_4` | `3003`, `4003`, `5003`, `6003` | `release` |
| `press_2` | `2002` | `off` |
| `press_3` | `3002` | `on_full_brightness` |
| `press_4` | `4002` | `on_min_brightness` |
| `press_1_and_3` | `5002` | `on_full_color_temp` |
| `press_2_and_4` | `6002` | `on_min_color_temp` |
| `press_energy_bar` | `1001`, `2001` | `sync` |
|  | `1000`, `1003`, `2000`, `2003`, `3000`, `4000`, `5000`, `6000` | *No action* |
|  | `3001` | `hold_brightness_up` |
|  | `4001` | `hold_brightness_down` |
|  | `5001` | `hold_color_up` |
|  | `6001` | `hold_color_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: PTM215XLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: PTM215XLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: PTM215XLightController
  integration: deconz
  controller: my_controller
  light: light.my_entity_id
```
