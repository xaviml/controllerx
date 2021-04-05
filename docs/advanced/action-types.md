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
  <event>:
    action: toggle 

  # The previous action type can be reduced as:
  <event>: toggle

  ## Call services
  # Call any service the same way as it is done through `Developer Tools > Services` in HA
  <event>:
    service: script.my_script
    data:
      attr1: 42
      attr2: foo

  # `entity_id` can be passed directly like this or through `data`.
  # Additionally, if the service is within the same domain
  # (light, media_player, etc) as the main entity from the configuration,
  # and entity_id is not passed, then it will use the one from the configuration.
  # This is handy, so there is no need to repeat the same entity over and over.
  # Priority order for entity_id:
  # - Inside data
  # - In the same level as "service"
  # - From the main config if the domain matches
  <event>:
    service: light.turn_on
    entity_id: light.my_light 

  ## Scene activation
  # Activate any HA Scene
  <event>:
    scene: scene.my_scene

  ## Delay
  # `delay` is usefull when defining a list of actions, and you want
  # an action to be triggered after some defined time.
  # The value of the attribute only accepts seconds.
  <event>:
    - on_min_brightness # predefined action
    - delay: 5 # wait 5 seconds
    - on_full_brightness # predefined action
```

_The `<event>` key is the event from your controller and integration._

If an action is still executing (most likely because of a `delay` in place), and another of the same type gets fired, the previous one will be cancelled and a new one will be executed. This is not configurable and it works the same as [`mode: restart`](https://www.home-assistant.io/docs/automation/modes) from Home Assistant automations.

Actions will be executed sequentially, so keep in mind that if using predefined actions, it is not recommended to use a list of `hold` actions since they will be executed sequentially, and it will not result in an expected behaviour. This is because the `hold` actions are blocking operations and they will not be finished until a `release` action is fired.
