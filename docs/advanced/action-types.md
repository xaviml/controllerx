---
title: Action types
layout: page
---

_This page assumes you already know how the [`mapping` attribute](custom-controllers) works._

An action type is reduced version of [Script Syntax](https://www.home-assistant.io/docs/scripts) from Home Assistant. It allows to one or a sequence of actions to execute when an event is fired. The available action types are [predefined action](predefined-actions), call service, scene activation and delay.

```yaml
...
mapping: # or merge_mapping
  ## Predefined actions
  # `toogle` is a light predefined action
  event:
    action: toggle 

  # The previous action type can be reduced as:
  event: toggle

  ## Call services
  # You can call any Home Assistant service as you can do from `Developer Tools > Services`
  event:
    service: script.my_script
    data:
      attr1: 42
      attr2: foo

  # You can pass the `entity_id` directly like this or through `data`
  event:
    service: light.turn_on
    entity_id: light.my_light 

  ## Scene activation
  # You can activate any Home Assistant Scene you have already created
  event:
    scene: scene.my_scene

  ## Delay
  # `delay` is usefull when defining a list of actions, and you want
  # an action to be triggered after some defined time.
  # The value of the attribute only accepts seconds.
  event:
    - on_min_brightness # predefined action
    - delay: 5 # wait 5 seconds
    - on_full_brightness # predefined action
```

_The `event` key is the event from your controller and integration._

If an action is still executing (most likely because of a `delay` in place), and another of the same type gets fired, the previous one will be cancelled and a new one will be executed. This is not configurable and it works the same as [`mode: restart`](https://www.home-assistant.io/docs/automation/modes) for Home Assistant automations.
