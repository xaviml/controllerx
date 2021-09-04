---
title: Hold/Click modes
layout: page
---

_This page assumes you already know how the [`mapping` attribute](custom-controllers) and [predefined actions](predefined-actions) work._

A new feature that came with ControllerX v4.16.0 is the ability to configure the hold and click actions. Up until now, we had the `{hold,click}_{brightness,color_temp,white_color,...}_{up,down,toggle}` predefined actions like:

- `hold_brightness_toggle`
- `hold_color_up`
- `click_colortemp_up`
- `click_brightness_down`
- ...

They allow to use click (1 step) or hold (smooth dim) with different attributes and directions. However, it became difficult to expand and add more functionality, so now the `click` and `hold` actions can be configured as follows:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  integration: deconz
  controller: my_controller
  light: light.my_light
  merge_mapping:
    2001:
      action: click # [click, hold] This is the predefined action.
      attribute: brightness # [brightness, color_temp, white_value, color, xy_color]
      direction: up # [up, down, toggle (only for hold)]
      mode: stop # [stop, loop, bounce (only for hold)] Stepper mode
      steps: 10 # It overrides the `manual_steps` and `automatic_steps` global attributes
```

The fields are the following:

- **action**: This is the [predefined action](predefined-actions), which in this case is `click` or `hold`.
- **attribute**: Attribute we want to act on. The available values are: `brightness`, `color_temp`, `white_value`, `color`, and `xy_color`. However, `xy_color` will ignore the `mode` and `steps` attribute since it already loops through the color wheel.
- **direction**: Direction to start. Options are `up`, `down`, and `toggle`. In case of `click` action, it will not accept `toggle`.
  - **`up`**: It goes up.
  - **`down`**: It goes down.
  - **`toggle`**: It changes direction everytime the action is performed.
- **mode**: This is the stepper mode. Options are `stop`, `loop`, and `bounce`. In case of `click` action, it will not accept `bounce`.
  - **`stop`**: This is the default behaviour. It stops when it reaches the ends (min or max).
  - **`loop`**: It loops through all the values under the same direction, so when reaching the end, it will start over. For example, if you configure the brightness with direction `up`, it will go from the value is currently in until 255 (default max), and then it will start over (1 default min) without releasing the button. This `mode` will not unless there is a `release` action or it reaches the `max_loops` attribute (default is 50 steps).
  - **`bounce`**: It bounces the ends, so when reaching the end it will switch directions. For example, if you configure the brightness with direction `down`, it will go from the value is currently in until 1 (default min), then it will start going up until reaching 255 and bouncing back again. This `mode` will not unless there is a `release` action or it reaches the `max_loops` attribute (default is 50 steps).

As you can see, the configuration is much flexible, however, it adds more lines than using the direct predefined actions. For this reason, the predefined actions like `{hold,click}_{brightness,color_temp,white_color,...}_{up,down,toggle}` will not be removed, but ControllerX will not have more of these since now it can be configured differently. This means for example that this configuration:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  integration: deconz
  controller: my_controller
  light: light.my_light
  merge_mapping:
    2001:
      action: hold
      attribute: brightness
      direction: up
```

It is the same as:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  integration: deconz
  controller: my_controller
  light: light.my_light
  merge_mapping:
    2001:
      action: hold_brightness_up
```

The old predefined actions have `stop` as a default mode.
