---
title: How to extract the controller parameter
layout: page
---

### Zigbee2mqtt

The name you need to add to the `controller` parameter can be found in `Configuration > Integrations > MQTT` and then select the controller. Then you will see the action sensor that by default finishes in `_action` or `_click`. The parameter you need is the entity id of the sensor.

### deCONZ

In case of deCONZ, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `deconz_event` and start listening. Then press any button and you will see event of the button, you will need to copy the `id` inside the `data` object.

### ZHA

In case of ZHA, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `zha_event` and start listening. Then press any button and you will see event of the button, you will need to copy the `device_ieee` inside the `data` object. It is a number like the following 00:67:88:56:06:78:9b:3f.
