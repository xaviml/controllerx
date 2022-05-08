---
title: Entity groups
layout: page
---

_This is supported from ControllerX v4.14.0_

ControllerX allow for Entity Controllers (LightController, MediaPlayerController, CoverController, etc) to work with grouped entities.

All is needed is an entity with `entity_id` attribute with a list of entities controlled by the grouped entity. For example, we can use a group entity from [Group Integration](https://www.home-assistant.io/integrations/group/), or from [Light Group Integration](https://www.home-assistant.io/integrations/light.group/). ControllerX will read attribute from the main entity (the first one from the list), but will run the actions on the grouped entity.

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

Then, we could for example configure the following in apps.yaml file:

```yaml
example_app:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.livingroom
```

`light.livingroom_1` will be the main light that ControllerX will read from, but `light.livingroom` will be the grouped entity that ControllerX will perform the actions.

For example, if `light.livingroom_1` does not support `brightness`, but `light.livingroom_2` and `light.livingroom_3` do, then the configuration will not work because ControllerX will not be able to read `brightness` attribute from `light.livingroom_1`.
