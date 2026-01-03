---
layout: page
title: Installation
---

# AppDaemon installation

This installation guide assumes that ControllerX runs on [AppDaemon addon](https://github.com/hassio-addons/addon-appdaemon), which can be found in the addon store. If you prefer to use your own AppDaemon instance, you can find the latest ControllerX code in the [Manual](#manual) section.

_You can read [here](/controllerx/others/run-appdaemon) what's AppDaemon and why is needed._

## AppDaemon addon

First, we will need to install the AppDaemon from the `Add-on store`. This will create the following folder in your system `/addon_configs/a0d7b954_appdaemon`, which we will need to modify the `/addon_configs/a0d7b954_appdaemon/appdaemon.yaml` (e.g. File Editor addon):

```yaml
---
secrets: /homeassistant/secrets.yaml # (1)
appdaemon:
  latitude: X.XXXXXXX # (2)
  longitude: X.XXXXXXX
  elevation: XXXX
  time_zone: XXXXXXXX
  app_dir: /homeassistant/appdaemon/apps # (4)
  plugins:
    HASS:
      type: hass
http:
  url: http://127.0.0.1:5050
admin:
api:
hadashboard:
```

1. This line is important for AppDaemon to get the secrets from the correct path.
2. Substitute with the correct values, or leave the default ones.
3. This line is important for AppDaemon to get the correct apps path where HACS install ControllerX in.

Note that by this point the addon might fail since `/homeassistant/appdaemon` might not exists yet, but you can keep following the installation steps.

You can read more about these changes in [this GitHub discussion](https://github.com/xaviml/controllerx/discussions/874).

## Enabling MQTT plugin (optional)

In case of using Zigbee2MQTT integration, it is recommended to [enable MQTT plugin](/controllerx/others/enable-mqtt-plugin) since the default [HA sensor listener is now deprecated](/controllerx/others/z2m-ha-sensor-deprecated).

## ControllerX installation

You can proceed to install ControllerX either manually or through HACS in the `/homeassistant/appdaemon/apps/` folder.

### HACS

The easiest way to add this to your Home Assistant installation is using HACS with `Enable AppDaemon apps discovery & tracking` checked. If you don't have it enabled, go to `Configuration > Integrations > HACS (Options)`. You will find ControllerX in the `Automation` section on HACS. This will automatically add ControllerX in `/homeassistant/appdaemon/apps/`, and updates will be tracked by HACS and update within the same folder.

### Manual

Download the [latest version](https://github.com/xaviml/controllerx/releases/latest/download/controllerx.zip), and then place the `controllerx` folder in your machine `/homeassistant/appdaemon/apps/controllerx`. The `controllerx.py` needs to be in `/homeassistant/appdaemon/apps/controllerx/controllerx.py`.

## Setup `apps.yaml`

Once we have the addon and ControllerX installed, we can create `/homeassistant/appdaemon/apps/apps.yaml`, where we can [configure ControllerX](../configuration) in.
