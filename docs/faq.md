---
layout: page
title: Frequently asked questions
---

#### 1. I placed the configuration in configuration.yaml and it doesn't work

ControllerX depends on AppDaemon and all the configuration for AppDaemon apps goes to `/config/appdaemon/apps/apps.yaml` and not `/config/configuration.yaml`.

#### 2. I updated ControllerX to a new version and it does not work

When updating ControllerX, the AppDaemon server (or addon) needs to be restarted.
