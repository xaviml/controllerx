[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._

**_Note: If you installed ControllerX manually, remember to restart AppDaemon after updating to a new version._**

**_:warning: HACS no longer supports AppDaemon apps, so ControllerX installed through HACS won't get updates anymore. Check [Migrating from HACS](https://BASE_URL/controllerx/start/installation#migrating-from-hacs) to keep updating it._**

## :pencil2: Features

- New installation method: the [ControllerX app](https://BASE_URL/controllerx/start/installation#controllerx-app-recommended) for Home Assistant, with its own AppDaemon and ControllerX preinstalled. ControllerX updates with the app.
- Support for Python 3.14.
- Releases include a `controllerx.zip.sha256` file with the checksum of `controllerx.zip`.

<!--
## :video_game: New devices

- [XYZ](https://BASE_URL/controllerx/controllers/XYZ) - add device with Z2M support. [ #123 ]
-->

## :hammer: Fixes

- Fix compatibility with AppDaemon 4.5.16. [ #1357 ]
- Fix color temperature actions for Home Assistant 2026.3 and later, which only accept color temperature in Kelvin. [ #1349 ]
- [WXKG11LMSensorSwitch](https://BASE_URL/controllerx/controllers/WXKG11LMSensorSwitch) - fix the ZHA integration triggering an action from the on/off report instead of only from the click count. [ #1354 ]

## :scroll: Docs

- Rewrite the [installation](https://BASE_URL/controllerx/start/installation) page with the two installation methods (ControllerX app and manual installation in the AppDaemon app), and how to migrate from HACS.
- Remove HACS from the documentation.
- [Enable MQTT plugin](https://BASE_URL/controllerx/others/enable-mqtt-plugin) - add `client_id`, needed when the ControllerX app and the AppDaemon app connect to the same MQTT broker.

<!--
## :clock2: Performance
-->

<!--
## :wrench: Refactor
-->
