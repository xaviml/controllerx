---
title: Templating
layout: page
---

Templating can be used when we want to dynamically use some of the properties during action execution based on their current state. It leverages the [HA templating](https://www.home-assistant.io/docs/configuration/templating/) system with the same syntax. It can be used for these type of parameters:

- Device types (`light`, `media_player`, `switch`, `cover`)
- Predefined actions
- Scene activation
- Call services

### Examples

It can be used to get the current media player is playing. It assumes there is a sensor that already gets updated when the current media player changes.

{% set special = "{{ states('sensor.current_media_player') }}" %}

```yaml
example_app:
  module: controllerx
  class: E1810MediaPlayerController
  integration: z2m
  controller: sensor.my_controller
  media_player: "{{ special }}"
```

Get data for call services. For example, get a random effect for our WLED light.

{% set special = "{{ state_attr('light.wled', 'effect_list') | random }}" %}

```yaml
example_app:
  module: controllerx
  class: Controller
  integration: z2m
  controller: sensor.my_controller
  mapping:
    toggle:
      service: wled.effect
      data:
        entity_id: light.wled
        effect: "{{ special }}"
```
