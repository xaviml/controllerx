[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._

**_Note: If you installed ControllerX manually, remember to restart AppDaemon after updating to a new version._**

<!--
## :pencil2: Features
-->

<!--
## :video_game: New devices

- [XYZ](https://BASE_URL/controllerx/controllers/XYZ) - add device with Z2M support. [ #123 ]
-->

<!--
## :hammer: Fixes
-->

## :scroll: Docs

- [Enable MQTT plugin](https://BASE_URL/controllerx/others/enable-mqtt-plugin) - explain how to enable MQTT from the ControllerX app options, and how to make AppDaemon receive only the topics of your controllers.

## :clock2: Performance

- MQTT - ControllerX now subscribes to the topics of its controllers (`mqtt`, `tasmota` and `z2m` with `listen_to: mqtt`). This allows setting `client_topics: NONE` in the AppDaemon MQTT plugin, so AppDaemon only receives the messages ControllerX needs instead of every message in the broker. Read more [here](https://BASE_URL/controllerx/others/enable-mqtt-plugin).

<!--
## :wrench: Refactor
-->
