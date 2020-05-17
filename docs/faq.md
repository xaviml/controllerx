---
layout: page
title: Frequently asked questions
---

#### 1. I placed the configuration in configuration.yaml and it doesn't work

ControllerX depends on AppDaemon and all the configuration for AppDaemon apps goes to `/config/appdaemon/apps/apps.yaml` and not `/config/configuration.yaml`.

#### 2. I updated ControllerX to a new version and it does not work

When updating ControllerX, the AppDaemon server (or addon) needs to be restarted.

#### 3. I properly configured E1744 (symfonisk) with z2m but it doesn't work

From the zigbee2mqtt documentation is recommended to set the `debounce` attribute. However, when set it does not send an empty state and the state of the controller stays active instead of being removed. This causes problems to ControllerX, so if you want to use this controller, I recommend to remove the `debounce` attribute since ControllerX handles repeated events by itself already.

#### 4. I have a group of lights and it does not work properly

HA offers different ways to group lights, even each Light integration might have the option of grouping lights (like [Hue](https://www.home-assistant.io/integrations/hue/) integration). This is why ControllerX sticks to just one official way to group lights, which is the [Group](https://www.home-assistant.io/integrations/group/) integration. This means you will need to set up a group with your lights in your `configuration.yaml`. ControllerX will know is a group of lights because it will use the `group.XXXXX` domain. Furthermore, it will take the first light as a master light, so it will take its values (brightness, color) to change the group of lights.

This does not mean that any other integration will not work, but they might not work as expected, this is why [Group](https://www.home-assistant.io/integrations/group/) integration should be used if you want the expected ControllerX behaviour.

#### 5. Error: "Value for X attribute could not be retrieved from light Y"

This error is shown when the light has support for the X attribute (e.g. brightness or color_temp) and the attribute is not in the state attribute of the entity. You can check whether the attribute X is shown in the state attributes from the "Developer Tools > States".

#### 6. Light is not turning on to the previous brightness

Zigbee does not support transition natively to lights, so this attribute depends on the integration you have installed for your light. If you encountered this problem is because ControllerX, by default, sends the `transition` attribute to the light(s) through an HA call and the integration for your light does not support transition when turning on or off and it leads to an unexpected behaviour. In fact, if you go to AppDaemon logs, you will be able to see the service call that ControllerX does when pressing the buttons. You can then, replicate those calls on "Developer Tools > Services". These are the issues created related to this problem on the different integrations:

- [Zigbee2MQTT](https://github.com/Koenkk/zigbee-herdsman-converters/issues/1073) (FIXED)
- [Hue integration](https://github.com/home-assistant/core/issues/32894) (OPEN)

However, while the problem is not in the scope of ControllerX, there is a workaround that will help you fix this problem while losing the transition when turning on/off or toggeling. For this, you could add `add_transition_turn_toggle: false` to your controller configuration. This is an example:

```yaml
problem_fixed:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.bedroom
  add_transition_turn_toggle: false
```

This will keep using transition when changing brightness or color, but not when turning on/off the light.
