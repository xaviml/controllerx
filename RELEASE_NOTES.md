[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._
PRERELEASE_NOTE

:warning: You must use Home Assistant 2021.4 or higher for this release to be working properly.

## :pencil2: Features

- Add `volume_set` predefined action for `MediaPlayerController`. See [here](https://xaviml.github.io/controllerx/advanced/predefined-actions#media-player).
- Add `tts` predefined action for `MediaPlayerController`. See [here](https://xaviml.github.io/controllerx/advanced/predefined-actions#media-player).
- Add `supported_color_modes` attribute to Light controller. It allows to define the supported color mode as defined in [HA documentation](https://developers.home-assistant.io/docs/core/entity/light)


## :hammer: Fixes

- Stop reading supported color mode from `supported_features`, and read it from `supported_color_modes` light entity attribute. [ #342 ]

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

- [E1812](https://xaviml.github.io/controllerx/controllers/E1812) - add ZHA support [ #324 ]
-->
