---
layout: page
title: Frequently asked questions
---

#### 1. I grouped 2 or more lights and they do not work

When grouping lights, they need to be grouped with the [group](https://www.home-assistant.io/integrations/group/) integration and not with the [light group platform](https://www.home-assistant.io/integrations/light.group/). This is because ControllerX needs to distinguish when it's a group and when is just an individual light.

#### 2. I placed the configuration in configuration.yaml and it doesn't work

ControllerX depends on AppDaemon and all the configuration for AppDaemon apps goes to `/config/appdaemon/apps/apps.yaml` and not `/config/configuration.yaml`.
