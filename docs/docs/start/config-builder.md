---
title: Configuration builder
description: Generate the ControllerX configuration for apps.yaml step by step, by choosing your device, what to control and the integration.
---

# Configuration builder

Choose your device, what you want to control with it and the integration that receives its events. Then, copy the configuration into your [`apps.yaml`](configuration.md).

<div id="cx-builder" class="cx-builder">
  <noscript>The configuration builder needs JavaScript. You can build the configuration by hand following the steps below.</noscript>
</div>

## How the configuration is built

Every ControllerX app in `apps.yaml` links one controller with one entity, and it has the following shape:

```yaml
livingroom_controller: # (1)!
  module: controllerx
  class: E1810Controller # (2)!
  integration: # (3)!
    name: z2m
    listen_to: mqtt
  controller: livingroom_remote # (4)!
  light: light.livingroom # (5)!
```

1. A unique name for the app. It can be anything, but each app needs a different one.
2. The controller class. It depends on the device and on what you want to control (light, media player, switch, cover...). Find it in the page of your device in [supported controllers](../controllers/index.md).
3. The [integration](integrations/index.md) that receives the events from the device (Zigbee2MQTT, deCONZ, ZHA, etc.).
4. The controller ID. Each integration page explains how to find it.
5. The entity to control. The parameter name depends on the controller type: `light`, `media_player`, `switch` or `cover`. Read more in [type configuration](type-configuration.md).

The rest of the parameters are optional and are described in [configuration](configuration.md) and [type configuration](type-configuration.md).
