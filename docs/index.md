# ControllerX

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

This automation brings the following functionalities for different [devices](https://github.com/xaviml/controllerx/wiki/Supported-controllers):

- Turn on/Turn off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.
- Play/pause music
- Volume up/down for a media player.

## Quick examples

This project gives support now to controllers integrated with zigbee2mqtt, deCONZ and ZHA.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: group.livingroom_lights
```

This is a real example to control a media player with E1744 with deCONZ:

```yaml
bedroom_speaker:
  module: controllerx
  class: E1744MediaPlayerController
  controller: symfonisk_controller
  integration: deconz
  media_player: media_player.bedroom_speaker
```

