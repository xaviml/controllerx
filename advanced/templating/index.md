Templating can be used to set some parameters dynamically when an action is executed, based on the current state of Home Assistant. It uses the [HA templating](<https://www.home-assistant.io/docs/configuration/templating/>) system with the same syntax. It can be used for these types of parameters:

- Device types (`light`, `media_player`, `switch`, `cover`)
- Predefined actions
- Scene activation
- Call services

## Examples

It can be used to control the media player that is currently playing. This example assumes there is a sensor that gets updated when the current media player changes.

```
example_app:
  module: controllerx
  class: E1810MediaPlayerController
  controller: my_controller
  integration:
    name: z2m
    listen_to: mqtt
  media_player: "{{ states('sensor.current_media_player') }}"
```

It can also be used to get data for service calls. For example, to set a random effect on our WLED light.

```
example_app:
  module: controllerx
  class: Controller
  controller: my_controller
  integration:
    name: z2m
    listen_to: mqtt
  mapping:
    toggle:
      service: wled.effect
      data:
        entity_id: light.wled
        effect: "{{ state_attr('light.wled', 'effect_list') | random }}"
```
