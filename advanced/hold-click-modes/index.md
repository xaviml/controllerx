*This page assumes you already know how the [`mapping` attribute](<https://xaviml.github.io/controllerx/advanced/index.md>) and [predefined actions](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md>) work.*

Since ControllerX v4.16.0, the hold and click actions can be configured. Before that, there were only the `{hold,click}_{brightness,color_temp,white_color,...}_{up,down,toggle}` predefined actions like:

- `hold_brightness_toggle`
- `hold_color_up`
- `click_colortemp_up`
- `click_brightness_down`
- ...

They allow using click (1 step) or hold (smooth dim) with different attributes and directions. However, it became difficult to extend them with more functionality, so the `click` and `hold` actions can now be configured as follows:

```
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

- **action**: This is the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md>), which in this case is `click` or `hold`.
- **attribute**: Attribute we want to act on. The available values are: `brightness`, `color_temp`, `white_value`, `color`, and `xy_color`. However, `xy_color` will ignore the `mode` and `steps` attributes since it already loops through the color wheel.
- **direction**: Direction to start. Options are `up`, `down`, and `toggle`. The `click` action does not accept `toggle`.
- **`up`**: It goes up.
- **`down`**: It goes down.
- **`toggle`**: It changes direction every time the action is performed.
- **mode**: This is the stepper mode. Options are `stop`, `loop`, and `bounce`. The `click` action does not accept `bounce`.
- **`stop`**: This is the default behaviour. It stops when it reaches either end (min or max).
- **`loop`**: It loops through all the values under the same direction, so when reaching the end, it will start over. For example, if you configure the brightness with direction `up`, it will go from the current value up to 255 (default max), and then it will start over from 1 (default min) without releasing the button. This `mode` will not stop unless there is a `release` action or it reaches the `max_loops` attribute (default is 50 steps).
- **`bounce`**: It bounces at the ends, so when reaching an end it switches direction. For example, if you configure the brightness with direction `down`, it will go from the current value down to 1 (default min), then it will start going up until reaching 255, and then bounce back again. This `mode` will not stop unless there is a `release` action or it reaches the `max_loops` attribute (default is 50 steps).

As you can see, the configuration is much more flexible, but it needs more lines than the direct predefined actions. For this reason, the predefined actions like `{hold,click}_{brightness,color_temp,white_color,...}_{up,down,toggle}` will not be removed, but no new ones will be added, since they can now be configured this way. For example, this configuration:

```
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

is the same as:

```
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
