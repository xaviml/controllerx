---
title: Shelly
layout: page
---

This integration ([**`shelly`**](https://www.home-assistant.io/integrations/shelly)) listens to `shelly.click` events. It creates an action like `<click_type>_<channel>`. It does not have any additional arguments.

## Parameters

| Parameter | Description       | Default  |
| --------- | ----------------- | -------- |
| `name`\*  | Integration name. | `shelly` |

_\* Required fields_

## How to extract the `controller` attribute

To extract the controller ID for Shelly, you can go to `Developer Tools > Events` then down the bottom you can subscribe for `shelly.click` and start listening. Then, press any button and you will see the event of the button, you will need to copy the `device` inside the `data` object. You can read more about the event [here](https://www.home-assistant.io/integrations/shelly/#events).
