---
title: Shelly
description: Configure ControllerX with the Shelly integration (shelly.click events) and find the controller ID of your device.
---

This integration ([**`shelly`**](https://www.home-assistant.io/integrations/shelly)) listens to `shelly.click` events. It creates an action like `<click_type>_<channel>`. It does not have any additional arguments.

## Parameters

| Parameter | Description       | Default  |
| --------- | ----------------- | -------- |
| `name`\*  | Integration name. | `shelly` |

_\* Required fields_

## How to extract the `controller` attribute

To find the controller ID for Shelly, go to `Developer Tools > Events`, subscribe to `shelly.click` at the bottom of the page and start listening. Then, press any button on the controller and copy the `device` from the `data` object of the event. You can read more about the event [here](https://www.home-assistant.io/integrations/shelly/#events).
