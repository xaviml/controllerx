---
title: Examples
layout: page
---

The purpose of this page is to show some real examples for the configuration. These are configurations placed in `/config/appdaemon/apps/apps.yaml`

E1524/E1810 controller with z2m that controls all the livingroom lights.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: group.livingroom_lights
```

Controlling a media player with E1744 with deCONZ:

```yaml
bedroom_speaker:
  module: controllerx
  class: E1744MediaPlayerController
  controller: symfonisk_controller
  integration: deconz
  media_player: media_player.bedroom_speaker
```

Controlling a light (just on/off) with E1743 with ZHA:

```yaml
bedroom_speaker:
  module: controllerx
  class: E1743Controller
  controller: 00:67:88:56:06:78:9b:3f
  integration: zha
  media_player: light.simple_light
  actions:
    - on
    - off
```

Controlling two lights with Aqara double key wireless switch (z2m):

```yaml
controller_left_switch:
  module: controllerx
  class: DoubleKeyWirelessAqaraController
  controller: sensor.controller_action
  light: light.light1
  integration: z2m
  manual_steps: 7
  actions:
    - left
    - left_double
    - left_long

controller_right_switch:
  module: controllerx
  class: DoubleKeyWirelessAqaraController
  controller: sensor.controller_action
  light: light.light2
  integration: z2m
  manual_steps: 7
  actions:
    - right
    - right_double
    - right_long
```

Controlling just the color with E1810 and z2m because toggle and brightness is controlled with zigbee groups.

```yaml
nameOfYourInstanceApp:
  module: controllerx
  class: E1810Controller
  controller: sensor.controller_action
  integration: z2m
  light: light.light1
  actions:
    - arrow_left_hold
    - arrow_left_release
    - arrow_right_hold
    - arrow_right_release
    - arrow_right_click
    - arrow_left_click
```

Controlling a simple light with Lutron Caseta Pro Pico, but giving the light a slower transition of 800ms:

```yaml
example_app:
  module: controllerx
  class: LutronCasetaProPicoLightController
  integration: state
  controller: sensor.controller_action
  light: light.example_light
  transition: 800
```

Hue Bridge HA integration for the lights and z2m for E1810 IKEA controller.

```yaml
hallway_light_group_no_toggle:
  # all actions, but toggle/hold for smooth operation with light groups on Hue Bridge
  # use HA groups to control dimming and color/color temp change
  # use Hue bridge light group for even and syncronized on/off function 
  module: controllerx
  class: E1810Controller
  controller: sensor.0x90fd9ffffe17d796_action
  integration: z2m
  # transition: 1000 # transition attribute works on Hue bridge
  smooth_power_on: true
  light: group.hallway # HA group. ControllerX syncs values from first group entity with remaining entities in group
  actions:
    - arrow_left_hold
    - arrow_left_release
    - arrow_right_hold
    - arrow_right_release
    - arrow_right_click
    - arrow_left_click
    - brightness_up_click
    - brightness_down_click
    - brightness_up_release
    - brightness_down_release
    - brightness_up_hold
    - brightness_down_hold

hallway_light_group_toggle:
  # toggle/hold for smooth operation with light groups on Hue Bridge
  # use Hue bridge light group for even and syncronized on/off function 
  module: controllerx
  class: E1810Controller
  controller: sensor.0x90fd9ffffe17d796_action
  integration: z2m
  # transition: 1000 # transition attribute works on Hue bridge
  light: light.hallway # Hue light group. On/off completely in sync, as zigbee group commands are used by Hue bridge 
  actions:
    - toggle
    - toggle_hold
```

## Others

These are examples that are quite extensive and were extracted in separated pages:

- [Using Sonos/Symfonisk media player(s) with ControllerX](sonos)

## Advanced

Controlling different lights with the same controller depending where you are.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: controller_id
  integration: deconz
  light: light.light1
  constrain_input_select: input_select.where_am_i,livingroom

controller_bedroom:
  module: controllerx
  class: E1810Controller
  controller: controller_id
  integration: deconz
  light: light.light2
  constrain_input_select: input_select.where_am_i,bedroom

controller_bathroom:
  module: controllerx
  class: E1810Controller
  controller: controller_id
  integration: deconz
  light: light.light3
  constrain_input_select: input_select.where_am_i,bathroom
```

Extending the functionality of the smooth power onfor the E1810, so when clicked or hold each button when the light is off, it sets the light to its minimum or maximum brightness or color, depending on the button pressed. This assumes you have a light with support to color temperature.

```yaml
livingroom_light_on:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
  constrain_input_boolean: light.livingroom,on

livingroom_light_off:
  module: controllerx
  class: CustomLightController
  controller: sensor.livingroom_controller_action
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
  constrain_input_boolean: light.livingroom,off
```

Customising Aqara magic cube with deCONZ. The key values were extracted from the deCONZ section in [here](/controllerx/controllers/MFKZQ01LM) and the values were extracted from the [predefined media player action list](/controllerx/others/custom-controllers#custom-media-player-controller).

```yaml
example_app:
  module: controllerx
  class: CustomMediaPlayerController
  controller: my_magic_cube_id
  integration:
    name: deconz
    type: gesture
  media_player: media_player.livingroom_speaker
  mapping:
    1: play_pause # Shake
    8: click_volume_down # Rotate left
    7: click_volume_up # Rotate right
    3: next_track # Flip90
    4: previous_track # Flip180
```

Customise the E1810 to invert the click and hold actions and control a group of sonos devices. By default it skips track when pressing, whit this it skips source by pressing.

```yaml
sonos_speaker:
  module: controllerx
  class: CustomMediaPlayerController
  controller: sensor.0x90fd9ffffe0cbd69_action
  integration: z2m
  media_player: group.sonos_all
  mapping:
    toggle: play_pause
    brightness_up_click: click_volume_up
    brightness_down_click: click_volume_down
    brightness_up_hold: hold_volume_up
    brightness_down_hold: hold_volume_down
    brightness_up_release: release
    brightness_up_release: release
    arrow_right_click: next_source
    arrow_left_click: previous_source
    arrow_right_hold: next_track
    arrow_left_hold: previous_track
```
