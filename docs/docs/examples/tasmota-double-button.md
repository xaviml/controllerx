---
title: Tasmota - Control an RGB light with two buttons
layout: page
---

**Updated November, 2022.**

### CONTROL A SINGLE RGB LIGHT USING A TASMOTA DEVICE WITH TWO BUTTONS

This example shows how to control an RGB light using the `Button1` to decrease brightness, color temperature, and color, and the `Button2` to decrease brightness, color temperature, and color.
For that, and as explained in the [docs](https://xaviml.github.io/controllerx/controllers/TasmotaButton/), you should set `SetOption73 1` to detach the buttons from the relays you might have, and to make the device to publish MQTT messages instead.

#### Motivation

In most of my rooms, I have a Sonoff Mini behind the switch in the wall, connected to one or more Zigbee RGB bulbs. Then, I replaced the wall switches with double push buttons of the same brand and model (to keep aesthetics and have my wife's approval). The Sonoff Mini allows connecting a button to the terminal header, plus another button to GPIO16 on the board itself through a pin header used to activate the DIY mode, so I connected those two buttons to the Sonoff so I can control the bulbs without cutting the power when the switch is toggled.
I use the left button as `Button1`and the right button as `Button2`.

#### Requirements

Tasmota: v12.2.0 or newer

ControllerX: v4.24.0 or newer

#### This example will

- toggle light on low brightness and warm white on `Button1` single press
- toggle light on high brightness and warm white on `Button2` single press
- decrease light brightness when `Button1` is held
- increase light brightness when `Button2` is held
- decrease color temperature on `Button1` double pressed
- increase color temperature on `Button2` double pressed
- rotate XY color down on `Button1` triple pressed
- rotate XY color up on `Button2` triple pressed

#### ControllerX apps.yaml example

##### Button1 (decrease)

```yaml
test_light_down:
  module: controllerx
  class: TasmotaButtonLightController
  controller: stat/test_device/RESULT # define your device topic here
  integration:
    name: tasmota
    component: Button1
  light: light.example_light # define your own light entity
  manual_steps: 5
  merge_mapping:
    SINGLE:
      action: toggle
      attributes:
        brightness: 76
        color_temp: 500
    DOUBLE: click_colortemp_down
    TRIPLE: click_xycolor_down
    HOLD:
      action: hold_brightness_down
```

##### Button2 (increase)

```yaml
test_light_up:
  module: controllerx
  class: TasmotaButtonLightController
  controller: stat/test_device/RESULT # define your device topic here
  integration:
    name: tasmota
    component: Button2
  light: light.example_light # define your own light entity
  manual_steps: 5
  merge_mapping:
    SINGLE:
      action: toggle
      attributes:
        brightness: 254
        color_temp: 500
    DOUBLE: click_colortemp_up
    TRIPLE: click_xycolor_up
    HOLD:
      action: hold_brightness_up
```

_This example was provided by [@cmiguelcabral](https://github.com/cmiguelcabral)_
