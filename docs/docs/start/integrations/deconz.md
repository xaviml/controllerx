---
title: deCONZ
layout: page
---

ControllerX listens to `deconz_event` events and actions get fired by default with the `event` attribute from the `data` object. However, you can change the attribute to listen to by adding a `type` attribute. In addition, you can select which attribute to listen to (`id` or `unique_id`) with `listen_to`.

## Parameters

| Parameter   | Description                                                 | Default  |
| ----------- | ----------------------------------------------------------- | -------- |
| `name`\*    | Integration name.                                           | `deconz` |
| `listen_to` | Selects which attribute to listen to (`id` or `unique_id`). | `id`     |
| `type`      | The attribute to listen to.                                 | `event`  |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for deCONZ, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `deconz_event` and start listening. Then, press any button and you will see the event of the button, you will need to copy the `id` inside the `data` object.

## Example

```yaml
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
