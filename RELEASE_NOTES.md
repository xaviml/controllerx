[![downloads](https://img.shields.io/github/downloads/xaviml/controllerx/VERSION_TAG/total?style=for-the-badge)](http://github.com/xaviml/controllerx/releases/VERSION_TAG)

<!--:warning: This major/minor change contains a breaking change.-->

_This minor change does not contain any breaking changes._
_Note: Remember to restart the AppDaemon addon/server after updating to a new version._

## :pencil2: Features

- Add `Event` integration. This new integration allows us define the event we want to listen to, and which actions build from it. It is ideal for DYI devices. Read more about it [here](https://BASE_URL/controllerx/advanced/event-integration). [ #568 ]

## :hammer: Fixes

- Check if `source_list` is None before treating as array [ #550 ] @kheyse

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

- [E2002](https://BASE_URL/controllerx/controllers/E2002) - add Media Player support for ZHA. [ #531 ] @Langthjem
- [SK5700002228949](https://BASE_URL/controllerx/controllers/SK5700002228949) - add Light support for deCONZ. [ #528 ]
- [WXCJKG11LM](https://BASE_URL/controllerx/controllers/WXCJKG11LM) - add deCONZ support for Light controller. [ #553 ]
- [WXKG07LM](https://BASE_URL/controllerx/controllers/WXKG07LM) - add Z2M Light Controller support. [ #547 ]
- [PhilipsRDM002](https://BASE_URL/controllerx/controllers/PhilipsRDM002) - add support for Light and Z2M Light controller. [ #551 ]
- [WXKG15LM](https://BASE_URL/controllerx/controllers/WXKG15LM) - add support for Light, Z2M Light and Switch controller. [ #560 ] @Crocmagnon
- [TuYaERS10TZBVKAA](https://BASE_URL/controllerx/controllers/TuYaERS10TZBVKAA) - add support for Light, Z2M Light and Media Player controller. [ #559 ]
