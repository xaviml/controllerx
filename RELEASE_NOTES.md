[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

:warning: This minor change contains a breaking change.

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._

## :pencil2: Features

- Add Zigbee2MQTT Light Controller (`Z2MLightController`). Until now we had an option to listen from MQTT, but light commands will always go through HA Light integration. This new controller allows you to interact directly with Zigbe2MQTT commands to interact with your lights. This means that you can leverage the `hold` actions that Zigbee2MQTT offers with barely no lag and much more smoother than `Light Controller` hold actions. However, it is not as flexible and does not offer as many options as `Light Controller` does. Many of the existing devices now have support to `Z2MLightController`, and you can use it in the `class` as you can now use `LightController` as well. You can read more about it [here](https://BASE_URL/controllerx/others/zigbee2mqtt-light-controller). [ #118, #168 ]
- Allow passing the delay time (in seconds) to `release_delay` attribute. [ #497 ]

## :hammer: Fixes

- :warning: Change [Hue Dimmer](https://BASE_URL/controllerx/controllers/HueDimmer) mapping for Zigbee2MQTT to be compatible with `legacy: false` mapping. This option will need to be [enabled from Zigbee2MQTT](https://www.zigbee2mqtt.io/devices/324131092621.html#options). [ #496 ]
- :warning: Rename `W2049` controllers for `E2002` (e.g. `W2049LightController` is now `E2002LightController`). The old names can still be used, but they show a warning and will be removed in the future. [ #504 ]

<!--
## :clock2: Performance
-->

<!--
## :scroll: Docs
-->

<!--
## :wrench: Refactor
-->

## :video_game: New devices

- [HueSmartButton](https://BASE_URL/controllerx/controllers/HueSmartButton) - add Z2M support. [ #498 ]
