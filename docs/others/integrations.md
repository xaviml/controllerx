---
title: Integrations
layout: page
---

Integrations is a way to abstract the logic from the event extraction in ControllerX. Each integration is resposible for listening the state or event and decoding the events in a way that ControllerX understands. These are the current integrations:

- state: Listens for the state of a sensor and the action is fired with the changed event. It does not have any arguments
- z2m: This integration is for zigbee2mqtt. For now is the same as the state integration. It does not have any arguments
- deconz: It listens to events and actions gets fired by default with the `event` attribute from the `data` object. However, you can change the attribute to listen to by adding a `type` attribute. This is an example

```yaml
example_app:
  module: controllerx
  class: MFKZQ01LMLightController
  controller: magic_cube
  integration:
    name: deconz
    type: gesture
  light: light.example_light
```

- zha:This integrations listens to events and concatenates the command with the argument for the action string. It does not have any arguments
