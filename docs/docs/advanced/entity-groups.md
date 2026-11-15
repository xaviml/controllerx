---
title: Entity groups
description: How ControllerX controls groups of entities (Group and Light Group integrations) and which entity it reads the attributes from.
---

_This is supported since ControllerX v4.14.0_

ControllerX allows entity controllers (LightController, MediaPlayerController, CoverController, etc.) to work with grouped entities.

All that is needed is an entity with an `entity_id` attribute containing the list of entities controlled by the group. For example, we can use a group entity from the [Group integration](https://www.home-assistant.io/integrations/group/), or from the [Light Group integration](https://www.home-assistant.io/integrations/light.group/). ControllerX reads the attributes from the main entity (the first one in the list), but runs the actions on the grouped entity.

Let's imagine we have a Light Group entity (`light.livingroom`):

```yaml
light:
  - platform: group
    name: livingroom
    entities:
      - light.livingroom_1
      - light.livingroom_2
      - light.livingroom_3
```

Then, we could configure the following in the `apps.yaml` file:

```yaml
example_app:
  module: controllerx
  class: E2002LightController
  controller: livingroom_controller
  integration:
    name: z2m
    listen_to: mqtt
  light: light.livingroom
```

`light.livingroom_1` will be the main light that ControllerX reads from, but `light.livingroom` will be the grouped entity that ControllerX performs the actions on.

For example, if `light.livingroom_1` does not support `brightness`, but `light.livingroom_2` and `light.livingroom_3` do, then the configuration will not work because ControllerX will not be able to read the `brightness` attribute from `light.livingroom_1`.
