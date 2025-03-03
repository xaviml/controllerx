---
title: Tasmota
layout: page
---

This integration ([**`tasmota`**](https://tasmota.github.io)) listens for the MQTT topic sent from the `controller` attribute, and gets the action from the attribute defined in `component`.

## Parameters

| Parameter     | Description                                         | Default   |
| ------------- | --------------------------------------------------- | --------- |
| `name`\*      | Integration name.                                   | `tasmota` |
| `component`\* | The component we are listening to (e.g. `Button1`). | `-`       |
| `key`         | The key to retrieve the data from.                  | `Action`  |

_\* Required fields_

For this integration to work, SetOption73 (for Buttons) and SetOption114 (for Switches) need to be set in Tasmota.

Tasmota payload:

```json
{
  "Button1": {
    "Action": "TOGGLE"
  }
}
```

## How to extract the `controller` attribute

Tasmota integration relies on MQTT plugin, so the `controller` is the MQTT topic to listen to (e.g. `stat/tasmota_device/RESULT`).

## Example

```yaml
example_app:
  module: controllerx
  class: TasmotaButtonLightController
  controller: stat/tasmota_device/RESULT
  integration:
    name: tasmota
    component: Button1
  light: light.example_light
```
