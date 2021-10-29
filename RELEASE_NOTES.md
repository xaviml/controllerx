[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._
PRERELEASE_NOTE

## :pencil2: Features

- Add `previous_state` attribute to restrict when an action is performed depending on the previous state of the entity. This is just applicable for `state` and `z2m` (with not MQTT) integrations. [#366]
- Add `cover_duration` attribute. Duration of the cover to open and/or close in seconds, so `toggle_open` and `toggle_close` can stop the cover if the cover is still moving. This is recommended to be used when the cover does not report `opening` and `closing` states, otherwise, it is not necessary. [#368]

<!--
## :hammer: Fixes
-->

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

- [WXKG06LM](https://xaviml.github.io/controllerx/controllers/WXKG06LM) - add Z2M and deCONZ support
- [W2049](https://xaviml.github.io/controllerx/controllers/W2049) - add ZHA support @patrezp [#375]
