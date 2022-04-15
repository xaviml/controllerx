[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._
PRERELEASE_NOTE

:warning: Home Assistant >= 2022.4.3 should be used for IKEA devices with ZHA.

## :pencil2: Features

- Add `key` attribute for MQTT integration. It allows reading specific attribute for JSON payloads. Read more [here](https://xaviml.github.io/controllerx/others/integrations#mqtt).

## :hammer: Fixes

- [E1524_E1810](https://xaviml.github.io/controllerx/controllers/E1524_E1810) - Fix ZHA mapping for 2022.4.X Home Assistant
- [E1743](https://xaviml.github.io/controllerx/controllers/E1743) - Fix ZHA mapping for 2022.4.X Home Assistant
- [E1744](https://xaviml.github.io/controllerx/controllers/E1744) - Fix ZHA mapping for 2022.4.X Home Assistant
- [W2049](https://xaviml.github.io/controllerx/controllers/W2049) - Fix ZHA mapping for 2022.4.X Home Assistant
- [W2049](https://xaviml.github.io/controllerx/controllers/W2049) - Fix Z2M mapping for the Media Player support [ #396 ]

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

- [W2049](https://xaviml.github.io/controllerx/controllers/W2049) - add Media Player support for Z2M and deCONZ [ #396 ] @ayatollah
- [TS0043] (https://xaviml.github.io/controllerx/controllers/TS0043) - add device with Z2M support [ #442 ] @rschuiling
- [HM-PB-2-WM55-2] (https://xaviml.github.io/controllerx/controllers/HM-PB-2-WM55-2) - add device with Homematic support [ #421 ]
- [HM-PBI-4-FM] (https://xaviml.github.io/controllerx/controllers/HM-PBI-4-FM) - add device with Homematic support [ #421 ]
- [HM-PB-6-WM55] (https://xaviml.github.io/controllerx/controllers/HM-PB-6-WM55) - add device with Homematic support [ #421 ]
