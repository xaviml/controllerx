This integration ([**`tasmota`**](<https://tasmota.github.io>)) listens to the MQTT topic set in the `controller` attribute, and gets the action from the attribute defined in `component`.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `tasmota` |
| `component`\* | The component we are listening to (e.g. `Button1`). | `-` |
| `key` | The key to retrieve the data from. | `Action` |

*\* Required fields*

For this integration to work, SetOption73 (for Buttons) and SetOption114 (for Switches) need to be set in Tasmota.

Tasmota payload:

```
{
  "Button1": {
    "Action": "TOGGLE"
  }
}
```

## How to extract the `controller` attribute

The Tasmota integration relies on the [MQTT plugin](<https://xaviml.github.io/controllerx/others/enable-mqtt-plugin/index.md>), so the `controller` is the MQTT topic to listen to (e.g. `stat/tasmota_device/RESULT`).

## Example

```
example_app:
  module: controllerx
  class: TasmotaButtonLightController
  controller: stat/tasmota_device/RESULT
  integration:
    name: tasmota
    component: Button1
  light: light.example_light
```
