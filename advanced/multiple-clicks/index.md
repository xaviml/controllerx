*This page assumes you already know how the [`mapping` attribute](<https://xaviml.github.io/controllerx/advanced/index.md>) works.*

Some controllers fire events for double, triple (or even quadruple) clicks, but others only fire single click events. This feature allows you to manage multiple clicks virtually, especially for those single click events.

When adding a new custom mapping for your controller, you can use a token (`$`) to indicate how many times an event needs to occur for the action to be fired. Let's see an example:

```
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

This might be a silly example, but it is enough to highlight some points about this feature. In this configuration we see 2 actions: `brightness_up_click` (not "multi-clickable") and `toggle` ("multi-clickable"). We also see an attribute called `multiple_click_delay`, which indicates the delay (in milliseconds, 500 by default) before a multiple click action is triggered. Let's go over the following scenarios:

- `brightness_up_click` is clicked once: The `on` action will be triggered immediately, with no delay.
- `toggle` is clicked once: The `click_color_up` action will be triggered after 500ms. Also note that `toggle` and `toggle$1` are basically the same, so if both are present, the one with the token (`$`) prevails. So `click_color_down` will never be called.
- `toggle` is clicked twice (with less than 500ms between clicks): The `off` action will be triggered 500ms after the second click.

The next example shows a real use of this feature with the E1810 controller from IKEA.

```
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

This will keep the default mapping for the E1810 controller by using `merge_mapping` and add new actions when clicking the middle button 2 and 3 times, to toggle the fairy lights and the bedroom lamp.

Note that ControllerX registers the multiple-click events in the initialization phase by checking the events with `$`, so it records whether it needs to wait to trigger the multiple-click event or not. If the triggered event is not registered as multiple-clickable, then it will be triggered immediately. However, if the triggered event is multiple-clickable, then it will wait as long as specified in `multiple_click_delay` to detect whether another click is issued or not. If no second (n-th) click is registered, then the event is triggered. Therefore, all multi-clickable events will have a delay specified by `multiple_click_delay`.
