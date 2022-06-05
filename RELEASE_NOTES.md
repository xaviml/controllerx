[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

:warning: This minor change contains a breaking change.

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._
PRERELEASE_NOTE

## :pencil2: Features

- Allow passing the delay time (in seconds) to `release_delay` attribute. [ #497 ]

## :hammer: Fixes

- :warning: Change [Hue Dimmer](https://BASE_URL/controllerx/controllers/HueDimmer) mapping for Zigbee2MQTT to be compatible with `legacy: false` mapping. This option will need to be [enabled from Zigbee2MQTT](https://www.zigbee2mqtt.io/devices/324131092621.html#options). [ #496 ]

<!--
## :clock2: Performance
-->

<!--
## :scroll: Docs
-->

<!--
## :wrench: Refactor
-->

<!--
## :video_game: New devices

- [XYZ](https://xaviml.github.io/controllerx/controllers/XYZ) - add device with Z2M support. [ #123 ]
-->
