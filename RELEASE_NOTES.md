[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

:warning: This minor change contains a breaking change.

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._

## :pencil2: Features

Added compatibility to use Tasmota as controller when SetOption73 and/or SetOption114 are enabled.

## :hammer: Fixes

- :warning: Fixes mapping for `ICTCG1Controller` and `ICTCG1MediaPlayerController` for Zigbee2MQTT integration. It now defaults to the mapping exposed from the device when it is in `legacy: false` mode. [ #577 ]

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

- [ICTCG1](https://BASE_URL/controllerx/controllers/ICTCG1) - add support for Z2MLightController. [ #577 ]
