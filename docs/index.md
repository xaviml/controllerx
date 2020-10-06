---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

_Bring full functionality to light and media player controllers. From turning devices on/off to changing the color lights._

_ControllerX_ brings the following functionalities for different [controllers](/controllerx/controllers):

- Turn on/Turn off light(s) or switch(es)
- Toggle light(s) or switch(es)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness and color temperature
- Color loop changing if the light supports xy color.
- Play/pause music
- Volume up/down for a media player.

## Why _ControllerX_?

Solutions like zigbee2mqtt, deconz and zha have their pros and cons, but if there is something good about these solutions is that you remove the dependency of a propietary hub (e.g.: IKEA, Xiaomi, Philips). However, there is a downside about removing this dependency and it is that not only the propietary hubs let you integrate a controller with lights or media players, but it also gives a behaviour to them. Home Assistant is great and we love it, but when it comes to create complex automations, it gets tricky. This is why I created _ControllerX_ with AppDaemon and the Home Assistant plugin, to give the behaviour to the devices we lose when not having the original hub.

## Quick example

With just this configuration placed in `/config/appdaemon/apps/apps.yaml`, you can have the E1810 controller from IKEA (5 buttons one) connected to the bedroom light and be able to change the brightness and color temperature or color.

```yaml
livingroom_controller:
  module: controllerx
  class: E1810Controller
  controller: sensor.livingroom_controller_action
  integration: z2m
  light: light.bedroom
```

## Videos

- [E1810 (IKEA) controlling a light through MQTT](https://twitter.com/xaviml93/status/1292235973510733826)
- [Symfonisk controlling Chromecast volume](https://twitter.com/xaviml93/status/1278000379444240390)
- [Magic Xiaomi Cube controlling a colour light](https://twitter.com/xaviml93/status/1231542785486049280)
- [E1810 (IKEA) controlling a colour light with ZHA](https://twitter.com/xaviml93/status/1227573383489085440)
- [Symfonisk controlling Google Home mini](https://twitter.com/xaviml93/status/1216124464901115905)
- [Symfonisk controlling a light](https://twitter.com/xaviml93/status/1216297058581258240)
- [Showing the colour wheel from HA](https://twitter.com/xaviml93/status/1213978663294787595)
- [E1743 (IKEA) button as a cover controller](https://twitter.com/xaviml93/status/1279875564736741376)
- [E1810 (IKEA) as a TV remote](https://twitter.com/xaviml93/status/1279874124026970115)
- [Double click for the middle button for E1810 (IKEA)](https://twitter.com/xaviml93/status/1313238350913040384)

### 💡 **NOTE**

_ControllerX_ uses an async loop to make HA call services requests (e.g. to change the brightness, the color temperature, the xy color, the volume of a media player). This means that when a button is held, _ControllerX_ calls periodically HA services until a release action is fired.

If you use deCONZ integration and what you want is just to dim your lights smoothly, we recommend that you to use [this](https://github.com/Burningstone91/Hue_Dimmer_Deconz) AppDaemon app from [_@Burningstone91_](https://github.com/Burningstone91). It brighten/dim your lights with a deCONZ calls instead of an async loop, this means that deCONZ would handle the dimming for you. Furthermore, it allows you to customise the controller the same way you can do it with the `mapping` attribute in _ControllerX_.

## How to start?

- [Installation](/controllerx/start/installation)
- [Configuration](/controllerx/start/configuration)
- [Supported controllers](/controllerx/controllers)

## Advanced

- [Custom controllers](others/custom-controllers)
- [Multiple clicks](others/multiple-clicks)

## Others

- [Update instructions](/controllerx/others/update)
- [Integrations](others/integrations)
- [Controller types](/controllerx/start/type-configuration)
- [Real examples](/controllerx/examples)
- [How to extract the controller parameter](others/extract-controller-id)
- [What's AppDaemon and why I need it](others/run-appdaemon)
- [FAQ](faq)
