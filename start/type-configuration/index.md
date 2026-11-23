Each device supports one or more controller types, and the controller type defines what the device can control (a light, a media player, a switch or a cover).

Here you can check the specific parameters that each type of controller needs. Check the [configuration](<https://xaviml.github.io/controllerx/start/configuration/index.md>) page for the generic parameters.

## Light controller

This controller allows the devices to control a light or a group of lights. It allows you to:

- Turn on/off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color
- Smooth increase/decrease (holding button) of brightness and color
- Color loop changing if the light supports xy color.

| key | type | value | description |
| --- | --- | --- | --- |
| `light`\* | string \| dictionary | `group.livingroom_lights` or `light.kitchen` | The light (or group of lights) you want to control |
| `manual_steps` | int | 10 | Number of steps to go from min to max when clicking. If the value is 2 with one click you will set the light to 50% and with another one to 100%. |
| `automatic_steps` | int | 10 | Number of steps to go from min to max when holding a button (smooth functionality). |
| `min_brightness` | int | 1 | The minimum brightness to set to the light. |
| `max_brightness` | int | 255 | The maximum brightness to set to the light. |
| `min_white_value` | int | 1 | The minimum white value to set to the light. |
| `max_white_value` | int | 255 | The maximum white value to set to the light. |
| `min_color_temp` | int | 153 | The minimum color temperature to set to the light. |
| `max_color_temp` | int | 500 | The maximum color temperature to set to the light. |
| `smooth_power_on` | boolean | False | If `True` the associated light will be set to minimum brightness when brightness up is clicked or held and the light is off. |
| `delay` | int | [Controller specific](<https://xaviml.github.io/controllerx/controllers/index.md>) | Delay in milliseconds between the instructions sent to the light when holding a button (smooth functionality). If it is set to 0, you might get unexpected behavior. |
| `max_loops` | int | 50 | Maximum number of loops when holding. The loop will stop either with a release action or reaching the `max_loops` value. |
| `hold_release_toggle` | boolean | False | If `true`, a `hold` action will work as a release when another `hold` is running. This is useful when you have a button with just one action event and you want to use the hold-release feature, then you just need to map that event to a `hold` action. |
| `release_delay` | float | 0 | `release` actions will be delayed this amount of time (in seconds). This is to avoid cases where `release` is sent almost at the same time as `hold` actions. |
| `transition` | int | 300 | Time in milliseconds the light takes to transition from one state to another. |
| `add_transition` | boolean | True | If `true` adds transition if supported, otherwise it does not add the `transition` attribute. |
| `add_transition_turn_toggle` | boolean | True | If `false` does not add transition when turning on/off or toggling, otherwise it adds the `transition` attribute to the call. See [FAQ \#6](<https://xaviml.github.io/controllerx/faq/index.md#6-light-is-not-turning-on-to-the-previous-brightness>) for a further explanation on the use of this parameter. |
| `color_wheel` | string \| list | `default_color_wheel` | It defines the color wheel used when changing the xy color with click or hold actions. See the options below. |
| `supported_features` | int | `0b101100` or `44` | See [below](<#supported_features-field>) for the explanation. |
| `supported_color_modes` | list | `["xy", "rgb"]` | It overrides the `supported_color_modes` that can be found in light attributes. Values can be `color_temp`, `hs`, `xy`, `rgb`, `rgbw` and `rgbww`. |
| `update_supported_features` | boolean | False | If `true`, it will check the supported features field every time before calling any call service action. Useful in case the supported features of the device entity changes over time. |
| `hold_toggle_direction_init` | string | `up` | It indicates the first direction of the hold toggle actions (`up` or `down`). |

*\* Required fields*

*Light dictionary for the `light` attribute:*

| key | type | value | description |
| --- | --- | --- | --- |
| `name`\* | string | `light.kitchen` | The light (or group of lights) you want to control |
| `color_mode` | string | `auto` | This attribute can take `auto`, `xy_color` or `color_temp` as value. `auto` will check first if the light supports `xy_color` and then `color_temp`. `xy_color` will cycle through different colors infinitely. `color_temp` will change the color temperature attribute of the light. If a light supports both, you can pick which one to use for the light(s). |

*\* Required fields*

*Information about `color_wheel` attribute:*

This attribute can be either a string or a list. These are the possible string values:

| value | description |
| --- | --- |
| `default_color_wheel` | These are the 24 colors that appear in the Home Assistant color wheel. |
| `color_temp_wheel` | These are the xy colors translated from color temperature (2000K to 6488K). They were extracted from [here](<https://www.waveformlighting.com/files/blackBodyLocus_1.txt>). |

Otherwise, a custom xy color list can be defined like the following:

```
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

## Zigbee2MQTT Light controller

This controller (`Z2MLightController`) allows the devices to control Zigbee2MQTT lights. It allows you to:

- Turn on/off light
- Toggle light
- Manual increase/decrease of brightness and color
- Smooth increase/decrease (holding button) of brightness and color

You can read more about this specific controller [here](<https://xaviml.github.io/controllerx/others/zigbee2mqtt-light-controller/index.md>).

| key | type | value | description |
| --- | --- | --- | --- |
| `light`\* | string \| dictionary | `my_light` | The light you want to control. This is the Zigbee2MQTT friendly name of the light. |
| `click_steps` | float | 70 | Number of steps that are passed to Zigbee2MQTT for click actions. |
| `hold_steps` | float | 70 | Number of steps that are passed to Zigbee2MQTT for hold actions. |
| `transition` | float | 0.5 | Transition sent to Zigbee2MQTT when changing brightness or color temp. |
| `use_onoff` | bool | `false` | This allows click and hold actions to turn on/off the light when off or minimum brightness is reached. |

*\* Required fields*

*Light dictionary for the `light` attribute:*

| key | type | value | description |
| --- | --- | --- | --- |
| `name`\* | string | `my_light` | The light you want to control. This is the Zigbee2MQTT friendly name of the light. |
| `mode` | string | `ha` | This attribute can take `ha` or `mqtt`. On the one hand, `ha` will send the mqtt messages through Home Assistant with [`mqtt.publish` service](<https://www.home-assistant.io/docs/mqtt/service/#service-mqttpublish>). On the other hand, `mqtt` will send the MQTT messages through MQTT plugin from AppDaemon (hence skipping HA). |
| `topic_prefix` | string | `zigbee2mqtt` | MQTT base topic for Zigbee2MQTT MQTT messages. The topic sent will be `<topic_prefix>/<friendly_name>/set`. |

*\* Required fields*

## Media player controller

This allows you to control media players. It supports volume, play/pause and skipping forward/backward the track and the source.

| key | type | value | description |
| --- | --- | --- | --- |
| `media_player`\* | string | `group.livingroom_speakers` or `media_player.bedroom_speaker` | The media player (or group of media players) you want to control |
| `volume_steps` | int | 10 | Number of steps to go from min to max when clicking or holding. If the value is 2 with one click you will set the volume to 50% and with another one to 100%. |
| `delay` | int | [Controller specific](<https://xaviml.github.io/controllerx/controllers/index.md>) | Delay in milliseconds between the volume up/down instructions when holding a button. The maximum value is 1000, and if it is set to 0, you might get unexpected behavior. |
| `max_loops` | int | 50 | Maximum number of loops when holding. The loop will stop either with a release action or reaching the `max_loops` value. |
| `hold_release_toggle` | boolean | False | If `true`, a `hold` action will work as a release when another `hold` is running. This is useful when you have a button with just one action event and you want to use the hold-release feature, then you just need to map that event to a `hold` action. |
| `release_delay` | float | 0 | `release` actions will be delayed this amount of time. This is to avoid cases where `release` is sent almost at the same time as `hold` actions. |
| `supported_features` | int | `0b10111111` or `191` | See [below](<#supported_features-field>) for the explanation. |
| `update_supported_features` | boolean | False | If `true`, it will check the supported features field every time before calling any call service action. Useful in case the supported features of the device entity changes over time. |

*\* Required fields*

## Switch controller

This allows you to control `switch` entities as well as `input_boolean` and `binary_sensor`. It supports turning on/off and toggling.

| key | type | value | description |
| --- | --- | --- | --- |
| `switch`\* | string | `group.switches` or `switch.dishwasher` | The switch (or group of switches) you want to control |

*\* Required fields*

## Cover controller

This allows you to control covers. It supports opening, closing and stopping covers.

| key | type | value | description |
| --- | --- | --- | --- |
| `cover`\* | string | `group.all_covers` or `cover.kitchen` | The cover (or group of covers) you want to control |
| `open_position` | number | 100 | The open position (between 0 and 100) |
| `close_position` | number | 0 | The close position (between 0 and 100) |
| `cover_duration` | number | \- | Duration of the cover to open and/or close in seconds, so `toggle_open` and `toggle_close` can stop the cover if the cover is still moving. This is recommended to be used when the cover does not report `opening` and `closing` states, otherwise, it is not necessary. |
| `supported_features` | int | `0b10111111` or `191` | See [below](<#supported_features-field>) for the explanation. |
| `update_supported_features` | boolean | False | If `true`, it will check the supported features field every time before calling any call service action. Useful in case the supported features of the device entity changes over time. |

*\* Required fields*

### "supported\_features" field

This field will override the `supported_features` attribute from the entity (light, media player, etc). By default, ControllerX will check this value from Home Assistant, however, sometimes this attribute does not properly reflect the features that the entity supports. ControllerX automatically selects one action or another depending on this value, so it is important that it reflects the supported features. This is defined as a bit field in Home Assistant, so the binary representation of the number defines which features it supports. You can see the values for each entity below.

#### Light

| feature | value |
| --- | --- |
| EFFECT | 4 |
| FLASH | 8 |
| TRANSITION | 32 |

If you want to express support for everything, the value is `0b101100` or `44`.

#### Media player

| feature | value |
| --- | --- |
| PAUSE | 1 |
| SEEK | 2 |
| VOLUME\_SET | 4 |
| VOLUME\_MUTE | 8 |
| PREVIOUS\_TRACK | 16 |
| NEXT\_TRACK | 32 |
| TURN\_ON | 128 |
| TURN\_OFF | 256 |
| PLAY\_MEDIA | 512 |
| VOLUME\_STEP | 1024 |
| SELECT\_SOURCE | 2048 |
| STOP | 4096 |
| CLEAR\_PLAYLIST | 8192 |
| PLAY | 16384 |
| SHUFFLE\_SET | 32768 |
| SELECT\_SOUND\_MODE | 65536 |
| SUPPORT\_BROWSE\_MEDIA | 131072 |
| SUPPORT\_REPEAT\_SET | 262144 |
| SUPPORT\_GROUPING | 524288 |

If you want to express support for everything, the value is `0b1111111111110111111` or `524223`.

#### Cover

| feature | value |
| --- | --- |
| OPEN | 1 |
| CLOSE | 2 |
| SET\_COVER\_POSITION | 4 |
| STOP | 8 |
| OPEN\_TILT | 16 |
| CLOSE\_TILT | 32 |
| STOP\_TILT | 64 |
| SET\_TILT\_POSITION | 128 |

If you want to express support for everything, the value is `0b11111111` or `255`.
