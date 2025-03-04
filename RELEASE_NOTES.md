[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

:warning: This major/minor change contains a breaking change.

**_Note: Remember to restart the AppDaemon addon/server after updating to a new version._**

## :pencil2: Features

- Add [`event` sensor listener](https://BASE_URL/controllerx/start/integrations/zigbee2mqtt/#event-state-listen_to-event) to Zigbee2MQTT integration. [ #1090 ]
- Deprecate [HA sensor action listener](https://BASE_URL/controllerx/start/integrations/zigbee2mqtt/#ha-states-listen_to-ha) from Zigbee2MQTT integration. [ #1090 ]

## :video_game: New devices

- [E2123](https://BASE_URL/controllerx/controllers/E2123) - add ZHA support. [ #1109 ] @harrismck

## :hammer: Fixes

- [TS0043](https://BASE_URL/controllerx/controllers/TS0043) - fix cover mapping [ #1082 ] @ChristopheBraud
- [E2123](https://BASE_URL/controllerx/controllers/E2123) - fix media player mapping [ #1102 ] @sevorl

## :scroll: Docs

- Refactor [Integration page](https://BASE_URL/controllerx/start/integrations).

<!--
## :clock2: Performance
-->

## :wrench: Refactor

- :warning: Remove compatibility with Python 3.8. Minimum version is Python 3.9 now. This breaking change should only affect to those running AppDaemon on Python 3.8 or lower. If you are running AppDaemon add-on, this change does not affect you.
