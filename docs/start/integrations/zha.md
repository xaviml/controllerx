---
title: ZHA Integration
layout: page
---

This integration (**`zha`**) listens to `zha_event` events and actions get fired by default with the `command` attribute from the `data` object. However, you can change the attribute to listen to by adding a `type` attribute.

## Parameters

| Attribute | Description                  | Default   |
| --------- | ---------------------------- | --------- |
| `name`    | The name of the integration. |           |
| `type`    | The attribute to listen to.  | `command` |

### How to extract the `controller` attribute

To extract the controller ID for ZHA, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `zha_event` and start listening. Then, press any button and you will see the event of the button, you will need to copy the `id` inside the `data` object.

This is an example:

```yaml
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  controller: magic_cube
  integration:
    name: zha
    type: gesture # defaults to `command`
  light: light.example_light
```
