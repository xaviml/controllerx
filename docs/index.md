---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

ControllerX brings the following functionalities for different [controllers](controllers):

- Turn on/Turn off light(s)
- Toggle light(s)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.
- Play/pause music
- Volume up/down for a media player.

## Why ControllerX?

Solutions like zigbee2mqtt, deconz and zha have their pros and cons, but if there is something good about these solutions is that you remove the dependency of a propietary hub (e.g.: IKEA, Xiaomi, Philips). However, there is a downside about removing this dependency and it is that not only the propietary hubs let you integrate a controller with lights or media players, but it also gives a behaviour to them. Home assistant is great and we love it, but when it comes to create complex automations it gets tricky. This is why I created ControllerX with AppDaemon and the Home Assistant plugin, to give the behaviour to the devices we lose when not having the original hub.

## Quick example

With just this configuration, you can have the E1810 controller from IKEA (5 buttons one) connected to the bedroom light and be able to change the brightness and color temperature or color.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.bedroom
```

## How to start?

- [Installation](start/installation) or [Update](start/update)
- [Configuration](start/configuration)
- [Supported controllers](controllers)
