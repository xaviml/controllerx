---
title: Tasmota SwitchMode 11/12 Example
layout: page
---

### TASMOTA SWITCHMODE 11/12 WALL SWITCH IMPLEMENTATION WITH HOME ASSISTANT / CONTROLLERX

Want to make your 'dumb' wall switches smart and at the same time improve installation of smart lights WAF 👩‍🦰 ? Then the solution could be to 'Tasmotize' your wall switches, and use Home Asssistant with ControllerX app to control the smart light connected to that switch. With this setup, you'll be able to toggle and dim your lights directly from your wall switch. Today, many WIFI switches are so small, that they can fit behind wall outlets/switches or in ceiling outlets. Personally, I've used [Shelly One devices](https://shop.shelly.cloud/shelly-1-wifi-smart-home-automation#50) and [Itead Sonoff Mini's](https://www.itead.cc/sonoff-mini.html). Both are easy to flash with Tasmota using either USB-to-UART adapter or directly OTA. No soldering is actually needed these days. The flash part and build instructions are to comprehensive to elaborate on further in this documentation. Instructions are 'out there' - Google it! 😉

One of my Sonoff Mini installations behind a wall switch. Danish wall switch modules are typically not larger than appx. 50x50mm pr. module (outside measurements). I’ve LK Opus 66 installed, which is a slightly larger type measuring 66mm in width. Still I can squeeze a Sonoff Mini in behind a ‘typical’ double module wall switch. Shelly devices are a bit smaller, round in shape and in general easier to fit than the Sonoff Mini’s.

![switchmode11-12.jpeg](/controllerx/assets/img/switchmode11-12.jpeg)

One final warning: Using Shelly/Sonoff devices behind wall switches/outlets involves fiddling with HIGH VOLTAGE that could potentially INJURE OR KILL YOU, if not handled/installed correctly !! Furthermore, local building code might prohibit use of such devices in wall outlets and unauthorized installation will most likely be illegal in most countries. If you don't know EXACTLY what you're doing - then DON'T proceed with this project !! Now you've been warned !!

Following example is with a Shelly One device, placed in the wall socket behind the switch, to control an Ikea WS bulb in the ceiling outlet. The bulb is connected to Home Assistant via Zigbee2MQTT. I've refitted my wall switch with a spring, so it'll act like a push button.

The Switchmode11/12 option in Tasmota gives the user five different switch commands to be used for automation. With ControllerX only three commands are needed, as ControllerX internally controls changes in dimming direction. These commands are via MQTT send to a HA sensor, which is used directly in ControllerX as a 'virtual' switch.

#### Switchmode11/12 Tasmota output commands are:

```
Switchstate=2: toggle (Normal TOGGLE function. One single press)
Switchstate=4: inc-dec (HOLD function. Send after delay defined with Setoption32)
Switchstate=5: inv (INVERSE dim direction function. Not used in this implementation, as ControllerX handles this internally)
Switchstate=6: clear (Delayed RELEASE function. Send when button is released AFTER delay defined with Setoption32. Not used in this implementation)
Switchstate=7: clear (Normal RELEASE function. Send immediately after button is released
```

#### Requirements:

Tasmota: v8.3.1.2 or newer

ControllerX: v2.7.2 or newer

#### Shelly device Tasmota setup:

Module type: Shelly 1 (46)

#### Use switchmode 11 !!

#### Sonoff Mini device Tasmota setup:

Module type: Sonoff Basic (1)

GPIO4: Switch1 (9)

#### Use switchmode 12 !!

#### Setup MQTT sensor in HA's configuration.yaml:

```yaml
sensor:
  - platform: mqtt
      name: "tasmota"
      state_topic: "tasmota_topic"
```

#### Setup ControllerX app:

First example is with two separate controllers. This will also handle HOLD FROM LIGHTS OFF situation. Which, when lights are off, will SYNC light/lights when button is held for 0,8 sec.

##### ControllerX apps.yaml example no. 1:

```yaml
controller_switchmode11_on:
  module: controllerx
  class: CustomLightController
  controller: sensor.tasmota
  integration: state
  light: light.your_light # define your own light entity
  constrain_input_boolean: light.your_light,on # This whole configuration will work when the light is on
  mapping:
    toggle: toggle
    inc-dec: hold_brightness_toggle
    clear: release

controller_switchmode11_off:
  module: controllerx
  class: CustomLightController
  controller: sensor.tasmota
  integration: state
  light: light.your_light # define your own light entity
  constrain_input_boolean: light.your_light,off # This whole configuration will work when the light is off
  mapping:
    toggle: toggle
    inc-dec: sync
```

Second example is a more simple setup, where smooth_power_on is enabled instead, when button is held from lights off position.

##### ControllerX apps.yaml example no. 2:

```yaml
tasmota_switchmode11:
  module: controllerx
  class: CustomLightController
  controller: sensor.tasmota
  integration: state
  smooth_power_on: true # enable 'smooth power on' feature when button is held from lights off
  delay: 250 # change delay if you want faster/slower dimming response (default: 350 ms.)
  light: light.your_light # define your own light entity
  mapping:
    toggle: toggle
    inc-dec: hold_brightness_toggle
    clear: release
```

#### Setup needed commands and rules in Tasmota software via console:

```
Powerretain1 1    Retain Tasmota power settings i HA in event of power outage
Setoption1 1      Allow only single, double and hold press button actions
Setoption32 8     Delay for HOLD button (in 0,1 sec.). I use 8 = 0,8 sec.
Setoption34 50    Minimize delay between backlog commands to 50 ms. (Default 200 ms.)
Switchtopic 0     Disable switchtopic. Needed when using rules in Tasmota.
Switchmode1 11    Set Tasmota to switchmode11

RULE1 on switch1#state=2 do backlog publish tasmota_topic toggle;publish tasmota_topic endon
on switch1#state=7 do backlog publish tasmota_topic clear;rule3 1;publish tasmota_topic endon

RULE2
on Mqtt#Disconnected do rule1 0 endon
on Mqtt#Connected do rule1 1 endon

RULE3 5
on switch1#state=4 do backlog publish tasmota_topic inc-dec;publish tasmota_topic;rule3 0 endon
```

**NB: Note the extra decimal '5' in RULE3 !!**

**RULE1** sends the TOGGLE command via MQTT and afterwards immediately clears the sensor state with an empty payload (just like a physical button does). It also handles the CLEAR command when button is released, enables RULE3 and finally clears payload.

**RULE2** handles the 'fall back' to direct switch control if MQTT server is unavailable. Nice WAF feature, if HA/MQTT server is down. Then lights still can be toggled on/off using the wall switch.

**RULE3** sends the HOLD command, disables it selves (to ensure only one HOLD command is send) and finally clears payload.

RULE3 is set as 'run once' in Tasmota (with the decimal 5 after the rule number) to prevent some extra HOLD commands gets send before rule is disabled.

_This example was provided by [@htvekov](https://github.com/htvekov)_
