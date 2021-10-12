---
title: How to extract the controller parameter
layout: page
---

The purpose of this page is to indicate what value the `controller` attribute should have depending on the integration used. Click [here](integrations) to know more about the integrations.

#### Zigbee2MQTT

The name you need to add to the `controller` parameter can be found in `Configuration > Integrations > MQTT` and then select the controller. Then you will see the action sensor that by default finishes in `_action`. The parameter you need is the entity id of the sensor.

#### deCONZ

In case of deCONZ, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `deconz_event` and start listening. Then press any button and you will see event of the button, you will need to copy the `id` inside the `data` object.

#### ZHA

In case of ZHA, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `zha_event` and start listening. Then press any button and you will see event of the button, you will need to copy the `device_ieee` inside the `data` object. It is a number like the following 00:67:88:56:06:78:9b:3f.

#### MQTT

In case of using MQTT integration, the `controller` attribute must have the MQTT topic to listen from. It is important that the topic payload contains directly the action name and not a JSON. This means that in case of using the MQTT integration with a z2m controller, then the topic to listen to must be `zigbee2mqtt/<friendly name>/action` or `zigbee2mqtt/<friendly name>/click`. You can see the topic on the Zigbee2MQTT logs.
