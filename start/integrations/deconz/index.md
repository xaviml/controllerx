This integration (**`deconz`**) listens to `deconz_event` events, and the action is taken by default from the `event` attribute of the `data` object. You can change the attribute that contains the action with the `type` parameter. In addition, you can select which attribute identifies the controller (`id` or `unique_id`) with `listen_to`.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `deconz` |
| `listen_to` | Attribute that identifies the controller (`id` or `unique_id`). | `id` |
| `type` | Attribute that contains the action. | `event` |

*\* Required fields*

## How to extract the `controller` attribute

To find the controller ID for deCONZ, go to `Developer Tools > Events`, subscribe to `deconz_event` at the bottom of the page and start listening. Then, press any button on the controller and copy the `id` from the `data` object of the event.

## Example

```
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  controller: magic_cube
  integration:
    name: deconz
    listen_to: unique_id # defaults to `id`
    type: gesture # defaults to `event`
  light: light.example_light
```
