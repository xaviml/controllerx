---
title: Enable MQTT Plugin
layout: page
---

If we want to use the `mqtt` integration or the `listen_to: mqtt` from `z2m` integration as well as the `Z2MLightController`, we will need to activate the MQTT Plugin on the AppDaemon configuration. Depending on how you [installed ControllerX](/controllerx/start/installation), this file is in:

- ControllerX app: `/app_configs/d35634e3_controllerx/appdaemon.yaml`
- AppDaemon app: `/app_configs/a0d7b954_appdaemon/appdaemon.yaml`

We will need the add the following highlighted section in that file:

```yaml hl_lines="12-18"
---
appdaemon:
  latitude: X.XXXXXXX
  longitude: X.XXXXXXX
  elevation: XXXX
  time_zone: XXXXXXXX
  missing_app_warnings: 0 # (1)
  plugins:
    HASS:
      type: hass
      token: !env_var SUPERVISOR_TOKEN
    MQTT:
      type: mqtt
      namespace: mqtt # This is important
      client_id: controllerx # (2)
      client_host: core-mosquitto # (3)
      client_user: XXXXX # (4)
      client_password: !secret mqtt_password # (5)
http:
  url: http://0.0.0.0:5050
admin:
api:
```

1. Extra tip: you can add `missing_app_warnings` if you don't want any warning spam from ControllerX when starting AppDaemon.
2. A name no other MQTT client uses. Without it, AppDaemon connects as `appdaemon_mqtt_client`, so if both the ControllerX app and the AppDaemon app use MQTT, the broker keeps disconnecting one of them.
3. `core-mosquitto` if you use the Mosquitto broker app. Otherwise, the host of your MQTT broker without the port (e.g. 192.168.1.10).
4. You should be able to get user and password from MQTT broker.
5. Add `mqtt_password: <your password>` to `secrets.yaml`, next to `appdaemon.yaml` (or to the file set in `secrets:`, if your `appdaemon.yaml` has that line). You can also write the password here directly.

Then restart the ControllerX app or the AppDaemon app.
