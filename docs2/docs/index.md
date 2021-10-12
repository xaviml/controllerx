---
layout: home
---

_Create controller-based automations with ease to control your home devices and scenes._

_ControllerX_ brings the following functionalities for different [controllers](/controllerx/controllers):

- Turn on/Turn off any home device (light, switch, media player, etc.)
- Manual increase/decrease of brightness and color temperature
- Smooth increase/decrease (holding button) of brightness, color temperature, volume, etc.
- Color loop changing if the light supports xy color
- Play/pause music
- Open/close covers

## Why _ControllerX_?

Solutions like Zigbee2MQTT, deCONZ and ZHA have their pros and cons, but if there is something good about these solutions is that we can remove the dependency of a propietary hub (e.g.: IKEA, Xiaomi, Phillips). However, there is a downside about removing this dependency and it is that not only the proprietary hubs let you integrate a controller with lights or media players, but it also gives a behaviour to them. This is why we end up using Home Assistant automations, however when it comes to create complex automations like this kind, it gets tricky and difficult to maintain. This is where _ControllerX_ comes in together with AppDaemon, to give the behaviour to the devices we lose when not having the original hub as well as easily create automation focus on button events.

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

## How to start?

- [Installation](/controllerx/start/installation)
- [Configuration](/controllerx/start/configuration)
- [Supported controllers](/controllerx/controllers)

## Advanced

- [Custom mapping](advanced/custom-controllers)
  - [Action types](advanced/action-types)
  - [Predefined actions](advanced/predefined-actions)
  - [Multiple clicks](advanced/multiple-clicks)
  - [Hold/Click modes](advanced/hold-click-modes)
- [Templating](advanced/templating)
- [Entity Groups](advanced/entity-groups)

## Others

- [Update instructions](/controllerx/others/update)
- [Integrations](others/integrations)
- [Controller types](/controllerx/start/type-configuration)
- [Real examples](/controllerx/examples)
- [How to extract the controller parameter](others/extract-controller-id)
- [What's AppDaemon and why I need it](others/run-appdaemon)
- [FAQ](faq)

## Community

Thank you to all these people for putting out there content related to ControllerX:

- [/u/canaletto](https://community.home-assistant.io/u/canaletto/summary) - [canaletto.fr](https://canaletto.fr/post/home-assistant-rc-and-lights) (French)
- [/u/jones](https://community.home-assistant.io/u/jones/summary) - [triumvirat.org](https://www.triumvirat.org/posts/hass/hass-controllerx/) (German)
- [/u/fribse](https://community.home-assistant.io/u/fribse/summary) - [YouTube](https://youtu.be/ZVsibNcc_tw) (Danish)
