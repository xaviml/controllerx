---
title: Shelly for HASS
layout: page
---

This integration ([**`shellyforhass`**](https://github.com/StyraHem/ShellyForHASS)) listens to `shellyforhass.click` events. It creates an action like `<action_type>`. It does not have any additional arguments.

## Parameters

| Parameter | Description       | Default         |
| --------- | ----------------- | --------------- |
| `name`\*  | Integration name. | `shellyforhass` |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for Shelly for HASS, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `shellyforhass.click` and start listening. Then, press any button and you will see the event of the button, you will need to copy the `entity_id` inside the `data` object. You can read more about the event [here](https://github.com/StyraHem/ShellyForHASS#shellyforhassclick-020).
