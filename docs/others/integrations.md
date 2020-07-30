---
title: Integrations
layout: page
---

Integrations is a way to abstract the logic from the event extraction in ControllerX. Each integration is resposible for listening the state or event and decoding the events in a way that ControllerX understands. [Here](extract-controller-id) you can see which value the `controller` should have for each of this integrations:

#### State

This integration (**`state`**) listens for the state of a sensor and the action is fired with the changed event. You can add `attribute` parameter if you want to listen to state change on the state attribute level. Read more about the options in [here](https://appdaemon.readthedocs.io/en/latest/AD_API_REFERENCE.html#appdaemon.adapi.ADAPI.listen_state). An example could be:

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

#### Zigbee2MQTT

This integration(**`z2m`**) is meant to be used for zigbee2mqtt. It listens the states from the HA sensor entities. It does not have any additional arguments.

#### deCONZ

This integration(**`deconz`**) listens to events and actions gets fired by default with the `event` attribute from the `data` object. However, you can change the attribute to listen to by adding a `type` attribute. This is an example

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

#### ZHA

This integration(**`zha`**) listens to events and concatenates the command with the argument for the action string. It does not have any additional arguments.

#### MQTT

This integration(**`mqtt`**) listens for the topic sent from the `controller` attribute. Although this integration makes sense to use together with [custom controllers](custom-controllers), it works with the actions from zigbee2mqtt. This means that if you have a configuration like the following:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.bedroom
```

You can remove the layer of HA state and therefore gain some speed by changing it for:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  # This is the action topic from z2m
  controller: zigbee2mqtt/livingroom_controller/action
  integration: mqtt
  light: light.bedroom
```

By doing this, ControllerX will be listening directly from MQTT rather than Home Assistant (which listens from MQTT). Not only can you use this with zigbee2mqtt, but also with any other MQTT integration. However, it comes with the limitation that it expects the payload from the topic to be the action and not a JSON, this is why the example above we use `zigbee2mqtt/livingroom_controller/action` and not `zigbee2mqtt/livingroom_controller`. Last but not least, MQTT needs to be configured on `appdaemon.yaml` by adding the `MQTT` plugin, apart from the `HASS` plugin:

```yaml
plugins:
  HASS:
    type: hass
  MQTT:
    type: mqtt
    namespace: mqtt # This is important
    client_host: <Host without indicating the port (e.g. 192.168.1.10)>
    client_user: XXXXX
    client_password: XXXXX
```
