---
title: Integrations
layout: page
---

Integrations is a way to abstract the logic from the event extraction in ControllerX. Each integration is resposible for listening the state or event and decoding the events in a way that ControllerX understands. [Here](extract-controller-id) you can see which value the `controller` should have for each of this integrations:

#### Zigbee2MQTT

This integration(**`z2m`**) is meant to be used for zigbee2mqtt. It listens the states from the HA sensor entities. You can add `listen_to` attribute to indicate if it listens for HA states (`ha`) or MQTT topics (`mqtt`). Default is `ha`. If you want to use the `mqtt`, then you will need to change the `appdaemon.yaml` as it is stated in the `MQTT` integration section. Imagine we have the following configuration already created for a `z2m` controller listening to HA state:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.bedroom
```

Then, if we want to listen to the MQTT topic directly (skipping the HA state machine), we will need to change to:

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
    action_key: action # By default is `action` already
  light: light.bedroom
```

Three things to clarify when using the `z2m` integration listening to MQTT:

- `appdaemon.yaml` needs to be changed by adding the MQTT plugin (see `MQTT` section below).
- The Zigbee2MQTT friendly name from the z2m needs to be specified in the `controller` attribute.
- `action_key` is the key inside the topic payload that contains the fired action from the controller. It is normally `action` or `click`. By default will be `action`.
- `action_group` is a list of allowed action groups for the controller configuration. Read more about it [here](https://github.com/xaviml/controllerx/pull/150).

#### deCONZ

This integration(**`deconz`**) listens to `deconz_event` events and actions gets fired by default with the `event` attribute from the `data` object. However, you can change the attribute to listen to by adding a `type` attribute. In addition, you can select which attribute to listen to (`id` or `unique_id`) with `listen_to`. This is an example:

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

#### ZHA

This integration(**`zha`**) listens to `zha_event` events and concatenates the command with the argument for the action string. It does not have any additional arguments.

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

By doing this, ControllerX will be listening directly from MQTT rather than Home Assistant (which listens from MQTT). Not only can you use this with zigbee2mqtt, but also with any other MQTT integration. However, it comes with the limitation that it expects the payload from the topic to be the action and not a JSON, this is why the example above we use `zigbee2mqtt/livingroom_controller/action` and not `zigbee2mqtt/livingroom_controller`. Last but not least, MQTT needs to be configured on `appdaemon.yaml` by adding the `MQTT` plugin, apart from the `HASS` plugin. The whole file should look like the following:

```yaml
---
secrets: /config/secrets.yaml
appdaemon:
  latitude: X.XXXXXXX
  longitude: X.XXXXXXX
  elevation: XXXX
  time_zone: XXXXXXXX
  # You can add `missing_app_warnings` if you don't want any
  # warning spam from ControllerX when starting AppDaemon
  missing_app_warnings: 0
  plugins:
    HASS:
      type: hass
    MQTT:
      type: mqtt
      namespace: mqtt # This is important
      client_host: <Host without indicating the port (e.g. 192.168.1.10)>
      client_user: XXXXX
      client_password: XXXXX
http:
  url: http://127.0.0.1:5050
admin:
api:
hadashboard:
```

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

#### Lutron Caséta

This integration(**`lutron_caseta`**) listens to `lutron_caseta_button_event` events. It creates an action like `button_<number>_<action type>`. It does not have any additional arguments.
