---
title: State
layout: page
---

This integration (**`state`**) listens for the state of a sensor and the action is fired with the changed event. You can add `attribute` parameter if you want to listen to state change on the state attribute level. Read more about the options in [here](https://appdaemon.readthedocs.io/en/latest/AD_API_REFERENCE.html#appdaemon.adapi.ADAPI.listen_state).

## Parameters

| Parameter   | Description                                   | Default |
| ----------- | --------------------------------------------- | ------- |
| `name`\*    | Integration name.                             | `state` |
| `attribute` | The attribute to listen to for state changes. | `-`     |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for State, you can go to `Developer Tools > States` and find the entity id of the sensor you want to use.

## Example

Listening for the attribute `click` from the sensor `sensor.my_custom_button`:

```yaml
example_app:
  module: controllerx
  class: LightController
  controller: sensor.my_custom_button
  integration:
    name: state
    attribute: click
  light: light.example_light
  mapping:
    1_click: "on"
    2_click: "off"
```
