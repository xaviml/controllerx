---
title: Homematic
layout: page
---

This integration ([**`homematic`**](https://www.home-assistant.io/integrations/homematic)) listens to `homematic.keypress` events. It creates an action like `<action_type>_<channel>`. It does not have any additional arguments.

## Parameters

| Parameter | Description       | Default     |
| --------- | ----------------- | ----------- |
| `name`\*  | Integration name. | `homematic` |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for Homematic, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `homematic.keypress` and start listening. Then, press any button and you will see the event of the button, you will need to copy the `name` inside the `data` object.
