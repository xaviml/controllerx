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