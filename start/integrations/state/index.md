This integration (**`state`**) listens to the state changes of an entity, and the new state is used as the action. Add the `attribute` parameter if you want to listen to the changes of an attribute instead. Read more about the options [here](<https://appdaemon.readthedocs.io/en/latest/AD_API_REFERENCE.html#appdaemon.adapi.ADAPI.listen_state>).

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `state` |
| `attribute` | The attribute to listen to for state changes. | `-` |

*\* Required fields*

## How to extract the `controller` attribute

To find the controller ID for State, go to `Developer Tools > States` and find the entity ID of the sensor you want to use.

## Example

Listening for the attribute `click` from the sensor `sensor.my_custom_button`:

```
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
