# Tuya TS0044

![Tuya TS0044](<https://xaviml.github.io/controllerx/assets/controllers/TS0044.jpeg>)

- **Manufacturer:** Tuya
- **Device ID:** `TS0044`
- **Controller types:** [Light](<#light>) (`TS0044LightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TS0044>)

## Notes

Note that each button performs the same actions. This is because ControllerX is designed to control just one entity (light or media player). So, you can include the `actions` parameter to include the actions needed, or use the `mapping` attribute to define a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>). You can check [here](<https://github.com/xaviml/controllerx/issues/18#issuecomment-582535634>) for reference.

Also, this controller supports the hold action, but not release. This means that there are no smooth brightness changes when holding, just step by step every time it is held.

## Light

- **Class:** `TS0044LightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `1_single`, `2_single`, `3_single`, `4_single` | `toggle` |
| `1_double`, `2_double`, `3_double`, `4_double` | `click_brightness_up` |
| `1_hold`, `2_hold`, `3_hold`, `4_hold` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: TS0044LightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: TS0044LightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```
