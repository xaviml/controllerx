---
title: Controller types
layout: page
---

Each device supports a type of controller and this is what gives them the functionality over an entity. As for now, the two types of supported controllers are lights and media players.

Here you can check the specific parameters that each type of controller needs. Check the [configuration](configuration) page for the generic parameters.

## Light controller

This controller allows the devices to control light or group of lights. This allows you to:

- Turn on/off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color
- Smooth increase/decrease (holding button) of brightness and color
- Color loop changing if the light supports xy color.

| key                          | type                 | value                                           | description                                                                                                                                                                                                                                                               |
| ---------------------------- | -------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `light`\*                    | string \| dictionary | `group.livingroom_lights` or `light.kitchen`    | The light (or group of lights) you want to control                                                                                                                                                                                                                        |
| `manual_steps`               | int                  | 10                                              | Number of steps to go from min to max when clicking. If the value is 2 with one click you will set the light to 50% and with another one to 100%.                                                                                                                         |
| `automatic_steps`            | int                  | 10                                              | Number of steps to go from min to max when smoothing. If the value is 2 with one click you will set the light to 50% and with another one to 100%.                                                                                                                        |
| `min_brightness`             | int                  | 1                                               | The minimum brightness to set to the light.                                                                                                                                                                                                                               |
| `max_brightness`             | int                  | 255                                             | The maximum brightness to set to the light.                                                                                                                                                                                                                               |
| `min_white_value`            | int                  | 1                                               | The minimum white value to set to the light.                                                                                                                                                                                                                              |
| `max_white_value`            | int                  | 255                                             | The maximum white value to set to the light.                                                                                                                                                                                                                              |
| `min_color_temp`             | int                  | 153                                             | The minimum color temperature to set to the light.                                                                                                                                                                                                                        |
| `max_color_temp`             | int                  | 500                                             | The maximum color temperature to set to the light.                                                                                                                                                                                                                        |
| `smooth_power_on`            | boolean              | False                                           | If `True` the associated light will be set to minimum brightness when brightness up is clicked or hold ad light is off.                                                                                                                                                   |
| `delay`                      | int                  | [Controller specific](/controllerx/controllers) | Delay in milliseconds that takes between sending the instructions to the light (for the smooth functionality). Note that if leaving to 0, you might get uncommon behavior.                                                                                                |
| `max_loops`                  | int                  | 50                                              | Maximum number of loops when holding. The loop will stop either with a release action or reaching the `max_loops` value.                                                                                                                                                  |
| `hold_release_toggle`        | boolean              | False                                           | If `true`, a `hold` action will work as a release when another `hold` is running. This is useful when you have a button with just one action event and you want to use the hold-release feature, then you just need to map that event to a `hold` action.                 |
| `transition`                 | int                  | 300                                             | Time in milliseconds that takes the light to transition from one state to another one.                                                                                                                                                                                    |
| `add_transition`             | boolean              | True                                            | If `true` adds transition if supported, otherwise it does not adds the `transition` attribute.                                                                                                                                                                            |
| `add_transition_turn_toggle` | boolean              | True                                            | If `false` does not add transition when turning on/off or toggling, otherwise it adds the `transition` attribute to the call. See [FAQ #6](/controllerx/faq#6-light-is-not-turning-on-to-the-previous-brightness) for a further explanation on the use of this parameter. |
| `color_wheel`                | string \| list       | `default_color_wheel`                           | It defines the color wheel used when changing the xy color either when click or hold actions are used. Check down to know more about the options.                                                                                                                         |
| `supported_features`         | int                  | `0b101100` or `44`                            | See [below](#supported_features-field) for the explanation.                                                                                                                                                                                                               |
| `supported_color_modes`      | list                 | `["xy", "rgb"]`                                 | It overrides the `supported_color_modes` that can be found in light attributes. Values can be `color_temp`, `hs`, `xy`, `rgb`, `rgbw` and `rgbww`.                                                                                                                        |
| `update_supported_features`  | boolean              | False                                           | If `true`, it will check the supported features field everytime before calling any call service action. Useful in case the supported features of the device entity changes over the time.                                                                                 |

_\* Required fields_

_Light dictionary for the `light` attribute:_

| key          | type   | value           | description                                                                                                                                                                                                                                                                                                                                                         |
| ------------ | ------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`\*     | string | `light.kitchen` | The light (or group of lights) you want to control                                                                                                                                                                                                                                                                                                                  |
| `color_mode` | string | `auto`          | This attribute can take `auto`, `xy_color` or `color_temp` as value. `auto` will check first if the light supports `xy_color` and then `color_temp`. `xy_color` will cicle through different colors infinitely. `color_temp` will change the color temperature attribute of the light. If a light supports both, user can pick which action wants for the light(s). |

_\* Required fields_

_Information about `color_wheel` attribute:_

This attribute can be either an string or a list. These are the possible string values:

| value | description |
| `default_color_wheel` | These are the 24 colors that appear in the circle color of home assistant. |
| `color_temp_wheel` | These are the xy colors translated from color temperature (2000K to 6488K). They were extracted from [here](https://www.waveformlighting.com/files/blackBodyLocus_1.txt). |

Otherwise, a custom xy color list can be defined like the following:

```yaml
example_app:
  module: controllerx
  class: < device class or LightController >
  controller: < your controller id >
  integration: < your integration >
  light: light.your_light
  color_wheel:
    - [0.525, 0.411]
    - [0.167, 0.338]
    - [0.324, 0.329]
```

## Media player controller

This allows you to control media players. It supports volume, play/pause and skipping forward/backward the track and the source.

| key                         | type    | value                                                         | description                                                                                                                                                                                                                                               |
| --------------------------- | ------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `media_player`\*            | string  | `group.livingroom_speakers` or `media_player.bedroom_speaker` | The media player (or group of media players) you want to control                                                                                                                                                                                          |
| `volume_steps`              | int     | 10                                                            | Number of steps to go from min to max when clicking or holding. If the value is 2 with one click you will set the volume to 50% and with another one to 100%.                                                                                             |
| `delay`                     | int     | [Controller specific](/controllerx/controllers)               | Delay in milliseconds that takes between sending the volume up/down instructions. Note that the maximum value is 1000 and if leaving to 0, you might get uncommon behavior.                                                                               |
| `max_loops`                 | int     | 50                                                            | Maximum number of loops when holding. The loop will stop either with a release action or reaching the `max_loops` value.                                                                                                                                  |
| `hold_release_toggle`       | boolean | False                                                         | If `true`, a `hold` action will work as a release when another `hold` is running. This is useful when you have a button with just one action event and you want to use the hold-release feature, then you just need to map that event to a `hold` action. |
| `supported_features`        | int     | `0b10111111` or `191`                                         | See [below](#supported_features-field) for the explanation.                                                                                                                                                                                               |
| `update_supported_features` | boolean | False                                                         | If `true`, it will check the supported features field everytime before calling any call service action. Useful in case the supported features of the device entity changes over the time.                                                                 |

_\* Required fields_

## Switch controller

This allows you to control `switch` entities as well as `input_boolean` and `binary_sensor`. It supports turning on/off and toggling.

| key        | type   | value                                   | description                                           |
| ---------- | ------ | --------------------------------------- | ----------------------------------------------------- |
| `switch`\* | string | `group.switches` or `switch.dishwasher` | The switch (or group of switches) you want to control |

_\* Required fields_

## Cover controller

This allows you to control covers. It supports opening/closing and stop covers.

| key                         | type    | value                                 | description                                                                                                                                                                               |
| --------------------------- | ------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cover`\*                   | string  | `group.all_covers` or `cover.kitchen` | The cover (or group of covers) you want to control                                                                                                                                        |
| `open_position`             | number  | 100                                   | The open position (between 0 and 100)                                                                                                                                                     |
| `close_position`            | number  | 0                                     | The close position (between 0 and 100)                                                                                                                                                    |
| `supported_features`        | int     | `0b10111111` or `191`                 | See [below](#supported_features-field) for the explanation.                                                                                                                               |
| `update_supported_features` | boolean | False                                 | If `true`, it will check the supported features field everytime before calling any call service action. Useful in case the supported features of the device entity changes over the time. |

_\* Required fields_

### "supported_features" field

This field will override the `supported_features` attribute from the entity (light, media player, etc). By default, ControllerX will check this value from Home Assistant, however, there are times that this attribute does not reflect properly the features that the entity supports. ControllerX automatically will select one action or another depending on this value, this is why it's important that reflects the supported features. This is defined as a bit field in Home Assistant, so its binary representation of the number will defined which features it supports. You can see the values for each entity below.

#### Light

| feature     | value |
| ----------- | ----- |
| EFFECT      | 4     |
| FLASH       | 8     |
| TRANSITION  | 32    |

If you want to express support for everything, the value is `0b101100` or `44`.

#### Media player

| feature              | value  |
| -------------------- | ------ |
| PAUSE                | 1      |
| SEEK                 | 2      |
| VOLUME_SET           | 4      |
| VOLUME_MUTE          | 8      |
| PREVIOUS_TRACK       | 16     |
| NEXT_TRACK           | 32     |
| TURN_ON              | 128    |
| TURN_OFF             | 256    |
| PLAY_MEDIA           | 512    |
| VOLUME_STEP          | 1024   |
| SELECT_SOURCE        | 2048   |
| STOP                 | 4096   |
| CLEAR_PLAYLIST       | 8192   |
| PLAY                 | 16384  |
| SHUFFLE_SET          | 32768  |
| SELECT_SOUND_MODE    | 65536  |
| SUPPORT_BROWSE_MEDIA | 131072 |
| SUPPORT_REPEAT_SET   | 262144 |
| SUPPORT_GROUPING     | 524288 |

If you want to express support for everything, the value is `0b1111111111110111111` or `524223`.

#### Cover

| feature            | value |
| ------------------ | ----- |
| OPEN               | 1     |
| CLOSE              | 2     |
| SET_COVER_POSITION | 4     |
| STOP               | 8     |
| OPEN_TILT          | 16    |
| CLOSE_TILT         | 32    |
| STOP_TILT          | 64    |
| SET_TILT_POSITION  | 128   |

If you want to express support for everything, the value is `0b11111111` or `255`.
