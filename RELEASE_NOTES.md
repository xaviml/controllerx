[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._
PRERELEASE_NOTE

:warning: Home Assistant >= 2022.4.3 should be used for IKEA devices with ZHA.
:warning: Custom Controllers have been removed from code. They were deprecated in [v3.4.0](https://github.com/xaviml/controllerx/releases/tag/v3.4.0). Following classes are no longer available:

- `CustomLightController` (`LightController` should be used instead).
- `CustomMediaPlayerController` (`MediaPlayerController` should be used instead).
- `CustomSwitchController` (`SwitchController` should be used instead).
- `CustomCoverController` (`CoverController` should be used instead).
- `CallServiceController` (`Controller` should be used instead).

## :pencil2: Features

- Add `key` attribute for MQTT integration. It allows reading specific attribute for JSON payloads (works like `action_key` from Zigbee2MQTT integration). Read more [here](https://xaviml.github.io/controllerx/others/integrations#mqtt).
- Add [HomeMatic](https://www.home-assistant.io/integrations/homematic/) (`homematic`) integration. Read more [here](https://xaviml.github.io/controllerx/others/integrations#homematic). [ #421 ]
- Add `brightness_from_controller_level` predefined action for `LightController`. It changes the brightness of the light from the value sent by the controller `action_level` (if supported).
- Add `brightness_from_controller_angle` predefined action for `LightController`. It changes the brightness of the light from the value sent by the controller `action_rotation_angle` (if supported). This fires a `hold` action, so a `release` one will be needed to stop brightness change.
- Add `volume_from_controller_angle` predefined action for `MediaPlayerController`. It changes volume based on controller angle (if supported). This fires a `hold` action, so a `release` one will be needed to stop volume change.

## :hammer: Fixes

- Fixes bug related to `mode: restart`. Actions were not restarted properly over time.
- [E1524_E1810](https://xaviml.github.io/controllerx/controllers/E1524_E1810) - Fix ZHA mapping for 2022.4.X Home Assistant. [ #455, #457 ]
- [E1743](https://xaviml.github.io/controllerx/controllers/E1743) - Fix ZHA mapping for 2022.4.X Home Assistant. [ #455, #457 ]
- [E1744](https://xaviml.github.io/controllerx/controllers/E1744) - Fix ZHA mapping for 2022.4.X Home Assistant. [ #455, #457 ]
- [W2049](https://xaviml.github.io/controllerx/controllers/W2049) - Fix ZHA mapping for 2022.4.X Home Assistant. [ #455, #457 ]
- [W2049](https://xaviml.github.io/controllerx/controllers/W2049) - Fix Z2M mapping for the Media Player support. [ #396 ]
- [PTM215X](https://xaviml.github.io/controllerx/controllers/PTM215X) - Rename `Niko91004LightController` to `PTM215XLightController`. [ #420 ]

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

- [TS0043](https://xaviml.github.io/controllerx/controllers/TS0043) - add device with Z2M support. [ #442 ] @rschuiling
- [HM-PB-2-WM55-2](https://xaviml.github.io/controllerx/controllers/HM-PB-2-WM55-2) - add device with Homematic support. [ #421 ]
- [HM-PBI-4-FM](https://xaviml.github.io/controllerx/controllers/HM-PBI-4-FM) - add device with Homematic support. [ #421 ]
- [HM-PB-6-WM55](https://xaviml.github.io/controllerx/controllers/HM-PB-6-WM55) - add device with Homematic support. [ #421 ]
- [HM-Sen-MDIR-WM55](https://xaviml.github.io/controllerx/controllers/HM-Sen-MDIR-WM55) - add device with Homematic support. [ #421 ]
- [PTM215X](https://xaviml.github.io/controllerx/controllers/PTM215X) - Add Z2M support. [ #420 ]
- [SNZB-01](https://xaviml.github.io/controllerx/controllers/SNZB-01) - Add Z2M support. [ #460 ]
- [ZNXNKG02LM](https://xaviml.github.io/controllerx/controllers/ZNXNKG02LM) - Add Z2M support as a Light and Media Player controller. [ #430 ]
