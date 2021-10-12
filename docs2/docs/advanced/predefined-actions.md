---
title: Predefined actions
layout: page
---

_This page assumes you already know how the [`mapping` attribute](custom-controllers) works._

Here you can find a list of predefined actions (one of the [action types](action-types)) for each type of controller.

## Light

When using a [light controller](/controllerx/start/type-configuration#light-controller) (e.g. `E1743Controller`) or `LightController`, the following actions can be used as a predefined action:

| value                       | description                                                                                                                                                                              | parameters                                              |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `"on"`                      | It turns on the light                                                                                                                                                                    | - `attributes`: a mapping with attribute and value      |
| `"off"`                     | It turns off the light                                                                                                                                                                   |                                                         |
| `toggle`                    | It toggles the light                                                                                                                                                                     | - `attributes`: a mapping with attribute and value      |
| `toggle_full_brightness`    | It toggles the light, setting the brightness to the maximum value when turning on.                                                                                                       |                                                         |
| `toggle_full_white_value`   | It toggles the light, setting the white value to the maximum value when turning on.                                                                                                      |                                                         |
| `toggle_full_color_temp`    | It toggles the light, setting the color temperature to the maximum value when turning on.                                                                                                |                                                         |
| `toggle_min_brightness`     | It toggles the light, setting the brightness to the minimum value when turning on.                                                                                                       |                                                         |
| `toggle_min_white_value`    | It toggles the light, setting the white value to the minimum value when turning on.                                                                                                      |                                                         |
| `toggle_min_color_temp`     | It toggles the light, setting the color temperature to the minimum value when turning on.                                                                                                |                                                         |
| `release`                   | It stops `hold` actions                                                                                                                                                                  |                                                         |
| `on_full_brightness`        | It puts the brightness to the maximum value                                                                                                                                              |                                                         |
| `on_full_white_value`       | It puts the white value to the maximum value                                                                                                                                             |                                                         |
| `on_full_color_temp`        | It puts the color temp to the maximum value                                                                                                                                              |                                                         |
| `on_min_brightness`         | It puts the brightness to the minimum value                                                                                                                                              |                                                         |
| `on_min_white_value`        | It puts the white value to the minimum value                                                                                                                                             |                                                         |
| `on_min_color_temp`         | It puts the color temp to the minimum value                                                                                                                                              |                                                         |
| `set_half_brightness`       | It sets the brightness to 50%                                                                                                                                                            |                                                         |
| `set_half_white_value`      | It sets the white value to 50%                                                                                                                                                           |                                                         |
| `set_half_color_temp`       | It sets the color temp to 50%                                                                                                                                                            |                                                         |
| `sync`                      | It syncs the light(s) to full brightness and white colour or 2700K (370 mireds)                                                                                                          | - `brightness`<br>- `color_temp`<br>- `xy_color`        |
| `click`                     | It brights up/down accordingly with the `manual_steps` attribute, and allow to pass parameters through YAML config. You can read more about it [here](hold-click-modes)                  | - `attribute`<br>- `direction`<br>- `mode`<br>- `steps` |
| `click_brightness_up`       | It brights up accordingly with the `manual_steps` attribute                                                                                                                              |                                                         |
| `click_brightness_down`     | It brights down accordingly with the `manual_steps` attribute                                                                                                                            |                                                         |
| `click_white_value_up`      | It turns the white value up accordingly with the `manual_steps` attribute                                                                                                                |                                                         |
| `click_white_value_down`    | It turns the white value down accordingly with the `manual_steps` attribute                                                                                                              |                                                         |
| `click_color_up`            | It turns the color up accordingly with the `manual_steps` attribute                                                                                                                      |                                                         |
| `click_color_down`          | It turns the color down accordingly with the `manual_steps` attribute                                                                                                                    |                                                         |
| `click_colortemp_up`        | It turns the color temp up accordingly with the `manual_steps` attribute                                                                                                                 |                                                         |
| `click_colortemp_down`      | It turns the color temp down accordingly with the `manual_steps` attribute                                                                                                               |                                                         |
| `click_xycolor_up`          | It turns the xy color up accordingly with the `manual_steps` attribute                                                                                                                   |                                                         |
| `click_xycolor_down`        | It turns the xy color down accordingly with the `manual_steps` attribute                                                                                                                 |                                                         |
| `hold`                      | It brights up/down until release accordingly with the `automatic_steps` attribute, and allow to pass parameters through YAML config. You can read more about it [here](hold-click-modes) | - `attribute`<br>- `direction`<br>- `mode`<br>- `steps` |
| `hold_brightness_up`        | It brights up until release accordingly with the `automatic_steps` attribute                                                                                                             |                                                         |
| `hold_brightness_down`      | It brights down until release accordingly with the `automatic_steps` attribute                                                                                                           |                                                         |
| `hold_brightness_toggle`    | It brights up/down until release accordingly with the `automatic_steps` attribute and alternates in each click                                                                           |                                                         |
| `hold_white_value_up`       | It turns the white value up until release accordingly with the `automatic_steps` attribute                                                                                               |                                                         |
| `hold_white_value_down`     | It turns the white value down until release accordingly with the `automatic_steps` attribute                                                                                             |                                                         |
| `hold_white_value_toggle`   | It turns the white value up/down until release accordingly with the `automatic_steps` attribute and alternates in each click                                                             |                                                         |
| `hold_color_up`             | It turns the color up until release accordingly with the `automatic_steps` attribute                                                                                                     |                                                         |
| `hold_color_down`           | It turns the color down until release accordingly with the `automatic_steps` attribute                                                                                                   |                                                         |
| `hold_color_toggle`         | It turns the color up/down until release accordingly with the `automatic_steps` attribute and alternates in each click                                                                   |                                                         |
| `hold_colortemp_up`         | It turns the color temp up until release accordingly with the `automatic_steps` attribute                                                                                                |                                                         |
| `hold_colortemp_down`       | It turns the color temp down until release accordingly with the `automatic_steps` attribute                                                                                              |                                                         |
| `hold_colortemp_toggle`     | It turns the color temp up/down until release accordingly with the `automatic_steps` attribute and alternates in each click                                                              |                                                         |
| `hold_xycolor_up`           | It turns the xy color up until release accordingly with the `automatic_steps` attribute                                                                                                  |                                                         |
| `hold_xycolor_down`         | It turns the xy color down until release accordingly with the `automatic_steps` attribute                                                                                                |                                                         |
| `hold_xycolor_toggle`       | It turns the xy color up/down until release accordingly with the `automatic_steps` attribute and alternates in each click                                                                |                                                         |
| `xycolor_from_controller`   | It changes the xy color of the light from the value sent by the controller (if supported)                                                                                                |                                                         |
| `colortemp_from_controller` | It changes the color temperature of the light from the value sent by the controller (if supported)                                                                                       |                                                         |

## Media Player

When using a [media player controller](/controllerx/start/type-configuration#media-player-controller) (e.g. `E1743MediaPlayerController`) or `MediaPlayerController`, the following actions can be used as a predefined action:

| value               | description                                        | parameters                                                                                                                                                                                                         |
| ------------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `hold_volume_down`  | It turns the volume down until `release` is called |                                                                                                                                                                                                                    |
| `hold_volume_up`    | It turns the volume up until `release` is called   |                                                                                                                                                                                                                    |
| `click_volume_down` | It turns the volume down one step                  |                                                                                                                                                                                                                    |
| `click_volume_up`   | It turns the volume up one step                    |                                                                                                                                                                                                                    |
| `volume_set`        | It sets the volume to given level                  | - `volume_level`: volume level (from 0 to 1)                                                                                                                                                                       |
| `release`           | It calls `release` for `hold` actions              |                                                                                                                                                                                                                    |
| `play_pause`        | It toggles the play/pause media                    |                                                                                                                                                                                                                    |
| `next_track`        | It skips the track forward                         |                                                                                                                                                                                                                    |
| `previous_track`    | It skips the track backward                        |                                                                                                                                                                                                                    |
| `next_source`       | It changes to the next source                      |                                                                                                                                                                                                                    |
| `previous_source`   | It changes to the previous source                  |                                                                                                                                                                                                                    |
| `mute`              | It mutes the media player                          |                                                                                                                                                                                                                    |
| `tts`               | Text-to-Speech                                     | - `message`<br>- `service`: the service to call without "tts." (str; default: "google_translate_say")<br>- `cache` (bool; default: None)<br>- `language` (str; default: None)<br>- `options` (dict; default: None) |

## Switch

When using a [switch controller](/controllerx/start/type-configuration#switch-controller) (e.g. `E1743SwitchController`) or `SwitchController`, the following actions can be used as a predefined action:

| value    | description                        | parameters |
| -------- | ---------------------------------- | ---------- |
| `on`     | It turns the switch on             |            |
| `off`    | It turns the switch off            |            |
| `toggle` | It toggles the state of the switch |            |

## Cover

When using a [cover controller](/controllerx/start/type-configuration#cover-controller) (e.g. `E1743CoverController`) or `CoverController`, the following actions can be used as a predefined action:

| value          | description                                        | parameters |
| -------------- | -------------------------------------------------- | ---------- |
| `open`         | It opens the cover                                 |            |
| `close`        | It closes the cover                                |            |
| `stop`         | It stops the cover                                 |            |
| `toggle_open`  | It stops the cover if running and opens otherwise  |            |
| `toggle_close` | It stops the cover if running and closes otherwise |            |

# How to pass parameters

When passing parameters to predefined actions, we will nede to use the `action` keyword together with the parameters. This is an example to change the default parameters for `sync` action:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  integration: z2m
  controller: sensor.controller_action
  light: light.my_light
  merge_mapping:
    toggle_hold:
      action: sync
      brightness: 128
      color_temp: 153
```

And this is another example for the `toggle` action:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  integration: z2m
  controller: sensor.controller_action
  light: light.my_light
  merge_mapping:
    toggle:
      action: toggle
      attributes:
        brightness: 128
        xy_color: [0.323, 0.329]
```
