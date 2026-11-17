# Tuya TS0044F

![Tuya TS0044F](<https://xaviml.github.io/controllerx/assets/controllers/TS0044F.jpeg>)

- **Manufacturer:** Tuya
- **Device ID:** `TS0044F`
- **Controller types:** [Light](<#light>) (`TS0044FLightController`)
- **Integrations:** [Zigbee2MQTT](<https://xaviml.github.io/controllerx/start/integrations/zigbee2mqtt/index.md>) (`z2m`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TS0044F>)

## Notes

This device is very similar to the TS0044 Tuya, except that it doesn't support hold actions or double clicks.

Note that each button performs the same actions. This is because ControllerX is designed to control just one entity (light or media player). So, you can include the `actions` parameter to include the actions needed, or use the `mapping` attribute to define a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>). You can check [here](<https://github.com/xaviml/controllerx/issues/18#issuecomment-582535634>) for reference.

Since this controller doesn't support the hold action, there are no smooth brightness changes, just step by step every time it is pressed.

## Light

- **Class:** `TS0044FLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Zigbee2MQTT | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `"on"`, `"off"` | `toggle` |
| `brightness_step_up` | `click_brightness_up` |
| `brightness_step_down` | `click_brightness_down` |

### Example configuration

```
example_app:
  module: controllerx
  class: TS0044FLightController
  integration:
    name: z2m
    listen_to: mqtt
  controller: my_controller
  light: light.my_entity_id
```

```
example_app:
  module: controllerx
  class: TS0044FLightController
  integration:
    name: z2m
    listen_to: event
  controller: my_controller_action
  light: light.my_entity_id
```
