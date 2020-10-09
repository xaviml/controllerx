---
title: Multiple clicks
layout: page
---

_This page assumes you already know how the [`mapping` attribute](custom-controllers) works._

Some controllers allow events like double, triple (even quadruple) clicks, but others only allow single clicks events coming from the controller. This feature, then, allows you to virtually manage multiple clicks, especially for those single click events.

When adding a new custom mapping for your controller, you can use a new token (`$`) to indicate how many times an events needs to occur, so the action gets fired. Let's see an example:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: my_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.my_light
  multiple_click_delay: 500 # default
  mapping:
    brightness_up_click: "on"
    toggle: click_color_down
    toggle$1: click_color_up
    toggle$2: "off" 
```

This could be a silly example, but it is enough to remark some points about this feature. In this configuration we see 2 actions: `brightness_up_click` (not "multi-clickable") and `toggle` ("multi-clickable"). We also see an attribute called `multiple_click_delay`, which indicates the delay (in milliseconds and 500 by default) when a multiple click action should be trigger. Let's go over the next scenarios:
- `brightness_up_click` is clicked once: The `on` action will be triggered immidiately, with no delay.
- `toggle` is clicked once: The `click_color_up` action will be triggered after 500ms. Also noticed that `toggle` and `toggle$1` are basically the same, so if both are present, the one with the token (`$`) will be the prevalent. So `click_color_down` will never be called.
- `toggle` is clicked twice (with less than 500ms between clicks): The `off` action will be triggered in 500ms after the second click.

This next example will show a real use of this feature with the E1810 controller from IKEA.

```yaml
livingroom:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller
  integration: 
    name: z2m
    listen_to: mqtt
  light: light.livingroom_lamp
  smooth_power_on: true
  merge_mapping:
    toggle$2:
      service: light.toggle
      data:
        entity_id: light.livingroom_fairylights
    toggle$3:
      service: light.toggle
      data:
        entity_id: light.bedroom
```

This will keep the default mapping for the E1810 controller by using `merge_mapping` and add a new action when clicking 2 and 3 times the middle button to toggle the fairylights and the bedroom lamp.
