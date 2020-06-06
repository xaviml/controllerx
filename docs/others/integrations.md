---
title: Integrations
layout: page
---

Integrations is a way to abstract the logic from the event extraction in ControllerX. Each integration is resposible for listening the state or event and decoding the events in a way that ControllerX understands. These are the current integrations:

- **`state`** : Listens for the state of a sensor and the action is fired with the changed event. It does not have any additional arguments.
- **`z2m`** : This integration is for zigbee2mqtt. This integration allows 2 modes of controller pairing: `ha` or `mqtt`. With `ha` you will need to specify the sensor entity from Home Assistant, like the following:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: sensor.your_controller_action
  integration:
    name: z2m
    type: ha
  light: light.example_light
```

Note that this is the same as:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: sensor.your_controller_action
  integration: z2m
  light: light.example_light
```

because `state` takes by default `ha`. Then, if you want to use the MQTT integration, then you will need to specify the **friendly name** of the device from Zigbee2MQTT on the `controller` attribute:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: 0x14b4883ffa81c167
  integration:
    name: z2m
    state: mqtt
  light: light.example_light
```

This example shows the default friendly name of the device, but user might change it. ControllerX listens for `zigbee2mqtt/<controller>/action` topic. Last but not least, MQTT needs to be configured on `appdaemon.yaml` by adding the `MQTT` plugin, apart from the `HASS` plugin:

```yaml
plugins:
  HASS:
    type: hass
  MQTT:
    type: mqtt
    namespace: mqtt
    client_host: <Host without indicating the port (e.g. 192.168.1.10)>
    client_user: XXXXX
    client_password: XXXXX
```

- **`deconz`** : It listens to events and actions gets fired by default with the `event` attribute from the `data` object. However, you can change the attribute to listen to by adding a `type` attribute. This is an example

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

- **`zha`** : This integrations listens to events and concatenates the command with the argument for the action string. It does not have any additional arguments.
