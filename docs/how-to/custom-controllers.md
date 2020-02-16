---
title: Custom Controllers
layout: page
---

Custom controllers let you map controller events to actions. There are 3 type of custom controllers: `CustomLightController`, `CustomMediaPlayerController`, `CallServiceController`. All these controllers have in common the attribute `mapping`, which is a key-value map. The key defines the event fired from the controller (you can check these events in the individual pages from the [supported controllers](/controllerx/controllers)). The value is defined depending on each custom controller.

## Custom light controller

Class: `CustomLightController`

This controller lets you map controller events with predefined light actions. This custom controller is a [Light controller](/controllerx/start/type-configuration#light-controller), so it inheritance all its parameters. This is the list of predefined actions that can be mapped as a value in the key-value map from the `mapping` attribute.

| value                     | description                                                                                                  |
| ------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `on`                      | It turns on the light                                                                                        |
| `off`                     | It turns off the light                                                                                       |
| `toggle`                  | It toggles the light                                                                                         |
| `release`                 | It stops `hold` actions                                                                                      |
| `on_full_brightness`      | It puts the brightness to the maximum value                                                                  |
| `on_full_color_temp`      | It puts the color temp to the maximum value                                                                  |
| `on_min_brightness`       | It puts the brightness to the minimum value                                                                  |
| `on_min_color_temp`       | It puts the color temp to the minimum value                                                                  |
| `click_brightness_up`     | It brights up accordingly with the `manual_steps` attribute                                                  |
| `click_brightness_down`   | It brights down accordingly with the `manual_steps` attribute                                                |
| `click_brightness_toggle` | It brights up/down accordingly with the `manual_steps` attribute and alternating for each click              |
| `click_color_up`          | It turns the color temp up accordingly with the `manual_steps` attribute                                     |
| `click_color_down`        | It turns the color temp down accordingly with the `manual_steps` attribute                                   |
| `click_color_toggle`      | It turns the color temp up/down accordingly with the `manual_steps` attribute and alternating for each click |
| `click_colortemp_up`      | description                                                                                                  |
| `click_colortemp_down`    | description                                                                                                  |
| `click_colortemp_toggle`  | description                                                                                                  |
| `click_xycolor_up`        | description                                                                                                  |
| `click_xycolor_down`      | description                                                                                                  |
| `click_xycolor_toggle`    | description                                                                                                  |
| `hold_brightness_up`      | description                                                                                                  |
| `hold_brightness_down`    | description                                                                                                  |
| `hold_brightness_toggle`  | description                                                                                                  |
| `hold_color_up`           | description                                                                                                  |
| `hold_color_down`         | description                                                                                                  |
| `hold_color_toggle`       | description                                                                                                  |
| `hold_colortemp_up`       | description                                                                                                  |
| `hold_colortemp_down`     | description                                                                                                  |
| `hold_colortemp_toggle`   | description                                                                                                  |
| `hold_xycolor_up`         | description                                                                                                  |
| `hold_xycolor_down`       | description                                                                                                  |
| `hold_xycolor_toggle`     | description                                                                                                  |

### Example of CustomLightController

This is an example that uses the controller E1810 to put the brightness and color temperature to maximum when pressing the top or right button and to minumum when pressing the bottom or left ones. The key values where extracted from zigbee2mqtt section found in [here](/controllerx/controllers/E1524_E1810) and the values are from the list beforementioned.

```yaml
example_app:
  module: controllerx
  class: CustomLightController
  controller: sensor.controller_action
  integration: z2m
  light: light.livingroom
  mapping:
    toggle: toggle
    brightness_up_click: on_full_brightness
    brightness_down_click: on_min_brightness
    brightness_up_hold: on_full_brightness
    brightness_down_hold: on_min_brightness
    arrow_right_click: on_full_color_temp
    arrow_left_click: on_min_color_temp
    arrow_right_hold: on_full_color_temp
    arrow_left_hold: on_min_color_temp
```
