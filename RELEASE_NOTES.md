[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

:warning: This major/minor change contains a breaking change.

**_Note: Remember to restart the AppDaemon addon/server after updating to a new version._**

<!--
## :pencil2: Features
-->

## :video_game: New devices

- [Philips929002398602](https://BASE_URL/controllerx/controllers/Philips929002398602) - add ZHA support. [ #580 ] @cznewt @ScratMan
- [AdeoHRC99CZC045](https://BASE_URL/controllerx/controllers/AdeoHRC99CZC045) - add device with Z2M support. [ #648 ]
- [Prolight5412748727388](https://BASE_URL/controllerx/controllers/Prolight5412748727388) - add device with Z2M support. [ #657 ]
- [TuYaERS10TZBVKAA](https://BASE_URL/controllerx/controllers/TuYaERS10TZBVKAA) - fix class name for Media Player Controller.
- [TuYaERS10TZBVKAA](https://BASE_URL/controllerx/controllers/TuYaERS10TZBVKAA) - add ZHA support. [ #625 ]

## :hammer: Fixes

- :warning: Fix Z2M and deCONZ default mapping for [Philips929002398602](https://BASE_URL/controllerx/controllers/Philips929002398602) (Hue Dimmer v2). The power button (click and hold) toggles the light and the Hue button changes the color. If you use this device with a custom mapping using the `mapping` attribute, there is nothing to worry about. [ #580 ]
- Allow running configuration with null actions. [ #662 ]

## :scroll: Docs

- Device pages: show events with no actions assigned. [ #662 ]
- [WXKG11LMSensorSwitch](https://BASE_URL/controllerx/controllers/WXKG11LMSensorSwitch) - fix device image.

<!--
## :clock2: Performance
-->

## :wrench: Build

- Update the minimum supported Python version to 3.8.
