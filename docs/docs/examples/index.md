---
title: Examples
description: Real ControllerX configuration examples, from basic setups to advanced custom mappings, multiple clicks and templating.
---

This page shows some real configuration examples. These configurations are placed in your [`apps.yaml`](../start/configuration.md).

## Basic

E1524/E1810 controller with z2m event entities that controls all the living room lights.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller_action
  integration:
    name: z2m
    listen_to: event
  light: group.livingroom_lights
```

E1524/E1810 controller integrated with Zigbee2MQTT, but using `mqtt` directly instead of the `z2m` integration.

```yaml
office_light:
  module: controllerx
  class: E1810Controller
  controller: office_controller # This is the Z2M friendly name of the device
  integration:
    name: z2m
    listen_to: mqtt
  light: light.office
```

Controlling a media player with the E1744 and deCONZ:

```yaml
bedroom_speaker:
  module: controllerx
  class: E1744MediaPlayerController
  controller: symfonisk_controller
  integration: deconz
  media_player: media_player.bedroom_speaker
```

Controlling a light (just on/off) with the E1743 and ZHA:

```yaml
bedroom_light:
  module: controllerx
  class: E1743Controller
  controller: 00:67:88:56:06:78:9b:3f
  integration: zha
  light: light.simple_light
  actions:
    - "on"
    - "off"
```

Controlling two lights with the Aqara double key wireless switch (z2m):

```yaml
controller_left_switch:
  module: controllerx
  class: DoubleKeyWirelessAqaraController
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.light1
  manual_steps: 7
  actions:
    - left
    - left_double
    - left_long

controller_right_switch:
  module: controllerx
  class: DoubleKeyWirelessAqaraController
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.light2
  manual_steps: 7
  actions:
    - right
    - right_double
    - right_long
```

Controlling just the color with the E1810 and z2m, because toggle and brightness are controlled with Zigbee groups.

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.light1
  actions:
    - arrow_left_hold
    - arrow_left_release
    - arrow_right_hold
    - arrow_right_release
    - arrow_right_click
    - arrow_left_click
```

Controlling a simple light with the Lutron Caseta Pro Pico, but giving the light a slower transition of 800ms:

```yaml
example_app:
  module: controllerx
  class: LutronCasetaProPicoLightController
  integration: state
  controller: sensor.controller_action
  light: light.example_light
  transition: 800
```

Hue Bridge HA integration for the lights and z2m for the E1810 IKEA controller.

```yaml
hallway_light_group_no_toggle:
  # all actions, but toggle/hold for smooth operation with light groups on Hue Bridge
  # use HA groups to control dimming and color/color temp change
  # use Hue bridge light group for even and synchronized on/off function
  module: controllerx
  class: E1810Controller
  controller: "x90fd9ffffe17d796"
  integration:
    name: z2m
    listen_to: mqtt
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
  # use Hue bridge light group for even and synchronized on/off function
  module: controllerx
  class: E1810Controller
  controller: "x90fd9ffffe17d796"
  integration:
    name: z2m
    listen_to: mqtt
  # transition: 1000 # transition attribute works on Hue bridge
  light: light.hallway # Hue light group. On/off completely in sync, as zigbee group commands are used by Hue bridge
  actions:
    - toggle
    - toggle_hold
```

Regular use of the E1743 controller for a light, but delaying the `off` action by 10 seconds. A use case could be a switch at the beginning of a corridor, where we do not want the light to turn off until some time has passed.

```yaml
corridor_controller:
  module: controllerx
  class: E1743Controller
  controller: corridor_controller
  integration: deconz
  light: light.corridor
  action_delay:
    2002: 10
```

Using an xy color light bulb as a color temperature one when it supports color temperature.

```yaml
office:
  module: controllerx
  class: E1810Controller
  controller: office_controller # This is the Z2M friendly name of the device
  integration:
    name: z2m
    listen_to: mqtt
  light:
    name: light.office
    color_mode: color_temp
```

Using an xy color light bulb as a color temperature one when it does NOT support color temperature.

```yaml
office:
  module: controllerx
  class: E1810Controller
  controller: zigbee2mqtt/office_controller/action
  integration: mqtt
  light: light.office
  color_wheel: color_temp_wheel
```

## Advanced

Controlling different lights with the same controller depending on where you are.

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

Controlling different lights with the E1810 controller. Using brightness buttons for one light, arrows for another one and the center to turn off a group of lights.

```yaml
light1_controller:
  module: controllerx
  class: LightController
  controller: e1810_controller
  integration: deconz
  light: light.light1
  mapping:
    2002: "on"
    3002: "off"
    2001: hold_brightness_up
    2003: release
    3001: hold_brightness_down
    3003: release

light2_controller:
  module: controllerx
  class: LightController
  controller: e1810_controller
  integration: deconz
  light: light.light2
  mapping:
    4002: "on"
    5002: "off"
    4001: hold_brightness_down
    4003: release
    5001: hold_brightness_up
    5003: release

all_lights_controller:
  module: controllerx
  class: LightController
  controller: e1810_controller
  integration: deconz
  light: group.all_lights
  mapping:
    1002: "off"
```

Extending the smooth power on functionality of the E1810, so when each button is clicked or held while the light is off, it sets the light to its minimum or maximum brightness or color, depending on the button pressed. This assumes you have a light that supports color temperature.

```yaml
livingroom_light_on:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.livingroom
  constrain_input_boolean: light.livingroom,on

livingroom_light_off:
  module: controllerx
  class: LightController
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
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

Customising the Aqara magic cube with deCONZ. The keys were extracted from the deCONZ column of its [device page](../controllers/MFKZQ01LM.md), and the values from the [predefined media player action list](../advanced/predefined-actions.md#media-player).

```yaml
example_app:
  module: controllerx
  class: MediaPlayerController
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

Customising the Aqara magic cube with z2m. This uses the `mapping` attribute to turn on different HA scenes.

```yaml
cube_bedroom:
  module: controllerx
  class: Controller
  controller: cube_bedroom
  integration:
    name: z2m
    listen_to: mqtt
  mapping:
    flip90:
      service: scene.turn_on
      data:
        entity_id: scene.bedroom1
    flip180:
      service: scene.turn_on
      data:
        entity_id: scene.bedroom2
    tap:
      service: scene.turn_on
      data:
        entity_id: scene.bedroom3
```

Customising the Aqara WXKG01LM. We want to toggle the light, always turning it on with brightness 20 (min: 0, max: 255). For this, we create one app configuration for the default behaviour of the controller, excluding `single`, which toggles the light. Then, we create a custom controller with the `mapping` attribute to give a behaviour to the `single` action.

```yaml
mando_aqara_salon:
  module: controllerx
  class: WXKG01LMLightController
  controller: "0x00158d00027b6d79"
  integration:
    name: z2m
    listen_to: mqtt
  light: light.0x000d6ffffec2620d_light
  merge_mapping:
    single: # Give an action to the `single` event
      service: light.toggle
      data:
        entity_id: light.0x000d6ffffec2620d_light
        brightness: 20
```

Customising the E1810 to invert the click and hold actions and control a group of Sonos devices. By default, it skips the track when pressing; with this configuration, it skips the source instead.

```yaml
sonos_speaker:
  module: controllerx
  class: MediaPlayerController
  controller: "0x90fd9ffffe0cbd69"
  integration:
    name: z2m
    listen_to: mqtt
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

The next configuration shows the use of the multiple clicks functionality and `merge_mapping`. We want to use the E1810 for a light (`light.light1`), and toggle another light (`light.light2`) when clicking the toggle button twice. We could do this in one app configuration, as you can see in the [multiple clicks page](../advanced/multiple-clicks.md), but we will do it separately to show that the first configuration needs to change `toggle` to `toggle$1`, so it is detected as a multiple-clickable action. Otherwise, when the center button is clicked twice, it will also toggle `light.light1`.

```yaml
example_app_1:
  module: controllerx
  class: E1810Controller
  controller: my_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.light1
  merge_mapping:
    toggle$1: toggle

example_app_2:
  module: controllerx
  class: E1810Controller
  controller: my_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.light2
  mapping:
    toggle$2: toggle
```

The following configuration is a tricky one, but it also shows the power of ControllerX to adapt to any use case. Imagine we want the following for our Symfonisk controller (E1744) with deCONZ:

- 1 click: Toggle light on/off.
- 2 clicks: Toggle between (predefined) warm and cold white.
- 3 clicks: "Switch to alternate behavior". Instead of the default dimming behavior when turning left/right, it changes the color temperature: turning left makes the light colder (more blueish) and turning right makes it warmer (more reddish).
- Rotate left/right: This depends on the state set when clicking 3 times.

Assuming you have created the following input booleans in HA (`input_boolean.light_mode`, `input_boolean.light_colortemp_mode`), we can use the following configuration:

```yaml
example_app:
  module: controllerx
  class: E1744LightController
  controller: symfonisk_controller
  integration: deconz
  light: light.livingroom_lamp
  automatic_steps: 15
  delay: 150
  mapping:
    2001: hold_brightness_up # Right turn
    3001: hold_brightness_down # Left turn
    2003: release # Stop right turn
    3003: release # Stop left turn
  constrain_input_boolean: input_boolean.light_mode,on

example_app2:
  module: controllerx
  class: E1744LightController
  controller: symfonisk_controller
  integration: deconz
  light: light.livingroom_lamp
  automatic_steps: 15
  delay: 150
  mapping:
    2001: hold_color_up # Right turn
    3001: hold_color_down # Left turn
    2003: release # Stop right turn
    3003: release # Stop left turn
  constrain_input_boolean: input_boolean.light_mode,off

example_app3:
  module: controllerx
  class: E1744LightController
  controller: symfonisk_controller
  integration: deconz
  light: light.livingroom_lamp
  min_color_temp: 200
  mapping:
    1004: on_min_color_temp # 2 clicks
  constrain_input_boolean: input_boolean.light_colortemp_mode,on

example_app4:
  module: controllerx
  class: E1744LightController
  controller: symfonisk_controller
  integration: deconz
  light: light.livingroom_lamp
  max_color_temp: 400
  mapping:
    1004: on_full_color_temp # 2 clicks
  constrain_input_boolean: input_boolean.light_colortemp_mode,off

example_app5:
  module: controllerx
  class: E1744LightController
  controller: symfonisk_controller
  integration: deconz
  light: light.livingroom_lamp
  mapping:
    1002: toggle # 1 clicks
    1004: # 2 clicks
      service: input_boolean.toggle
      data:
        entity_id: input_boolean.light_colortemp_mode
    1005: # 3 clicks
      service: input_boolean.toggle
      data:
        entity_id: input_boolean.light_mode
```

The following example shows the potential of [templating](../advanced/templating.md). Let's say we want to execute different [predefined actions](../advanced/predefined-actions.md) every time we click a button (E1810 in this case). First, we can create an input select through the UI or YAML in HA:

```yaml
input_select:
  light_state:
    options:
      - on_min_brightness
      - on_full_brightness
      - set_half_brightness
```

Then, we can define the following ControllerX configuration to change the option of the input select and apply the selected predefined action:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.my_light
  mapping:
    toggle:
      - service: input_select.select_next
        data:
          entity_id: input_select.light_state
      - action: "{{ states('input_select.light_state') }}"
```
