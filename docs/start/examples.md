---
title: Examples
layout: page
---

The purpose of this page is to show some real examples for the configuration.

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
