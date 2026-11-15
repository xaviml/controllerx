---
title: Action types
description: Action types that can be used in a ControllerX mapping, including predefined actions, service calls, scenes and delays.
---

_This page assumes you already know how the [`mapping` attribute](index.md) works._

An action type is a reduced version of the Home Assistant [script syntax](https://www.home-assistant.io/docs/scripts). It defines one action or a sequence of actions to execute when an event is fired. The available action types are [predefined actions](predefined-actions.md), service calls, scene activation and delays.

```yaml
...
mapping: # or merge_mapping
  ## Predefined actions
  # `toggle` is a light predefined action
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
  # This is handy, so there is no need to repeat the same entity over and over again.
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
  # `delay` is useful when defining a list of actions, and you want
  # an action to be triggered after some defined time.
  # The value of the attribute only accepts seconds.
  <event>:
    - on_min_brightness # predefined action
    - delay: 5 # wait 5 seconds
    - on_full_brightness # predefined action
```

_The `<event>` key is the event from your controller and integration._

If an action is still executing (most likely because of a `delay`) and the same event gets fired again, the behaviour depends on the [`mode`](../start/configuration.md#parameters) parameter, which works like the [Home Assistant automation modes](https://www.home-assistant.io/docs/automation/modes). By default (`mode: single`), the new execution is ignored and a warning is logged. Use `mode: restart` to cancel the running action and start a new one.

Actions are executed sequentially, so it is not recommended to use a list of `hold` predefined actions, since it will not result in the expected behaviour. This is because `hold` actions are blocking operations, and they do not finish until a `release` action is fired.
