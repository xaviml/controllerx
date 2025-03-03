---
title: ZHA
layout: page
---

This integration (**`zha`**) listens to `zha_event` events and concatenates the command with the argument for the action string. It does not have any additional arguments.

## Parameters

| Parameter | Description       | Default |
| --------- | ----------------- | ------- |
| `name`\*  | Integration name. | `zha`   |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for ZHA, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `zha_event` and start listening. Then, press any button and you will see the event of the button, you will need to copy the `device_ieee` inside the `data` object. It is a number like the following 00:67:88:56:06:78:9b:3f.
