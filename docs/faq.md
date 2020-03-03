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
