---
title: Lutron Caséta
layout: page
---

This integration (**`lutron_caseta`**) listens to `lutron_caseta_button_event` events. It creates an action like `button_<number>_<action type>`. It does not have any additional arguments.

## Parameters

| Parameter | Description       | Default         |
| --------- | ----------------- | --------------- |
| `name`\*  | Integration name. | `lutron_caseta` |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for Lutron Caséta, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `lutron_caseta_button_event` and start listening. Then, press any button and you will see the event of the button, you will need to copy the relevant attribute inside the `data` object.
