---
title: Enable MQTT Plugin
description: Enable the AppDaemon MQTT plugin, needed by the mqtt and tasmota integrations, z2m with listen_to mqtt and the Zigbee2MQTT light controller.
---

If we want to use the `mqtt` or `tasmota` integrations, `listen_to: mqtt` in the `z2m` integration, or the `Z2MLightController` with `mode: mqtt`, we need to enable the AppDaemon MQTT plugin. How to do it depends on how you [installed ControllerX](../start/installation.md).

## ControllerX app

1. Go to **Settings → Apps → ControllerX → Configuration**.
2. Turn on **Enable MQTT**.
3. If you use the Mosquitto broker app, that's all: the app gets the broker address and credentials from Home Assistant. Otherwise, fill in **MQTT host** (without the port, e.g. `192.168.1.10`), **MQTT port**, **MQTT username** and **MQTT password**. They are under **Show unused optional configuration options**.
4. Save. Home Assistant offers to restart the app.

The app manages the AppDaemon configuration itself, so there's no `appdaemon.yaml` to edit.

## AppDaemon app

Add the following highlighted section to the AppDaemon configuration (`/app_configs/a0d7b954_appdaemon/appdaemon.yaml`):

```yaml hl_lines="12-19"
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
      client_id: appdaemon # (2)
      client_host: core-mosquitto # (3)
      client_user: XXXXX # (4)
      client_password: !secret mqtt_password # (5)
      client_topics: NONE # (6)
http:
  url: http://0.0.0.0:5050
admin:
api:
```

1. Extra tip: you can add `missing_app_warnings` if you don't want any warning spam from ControllerX when starting AppDaemon.
2. A name no other MQTT client uses. Without it, AppDaemon connects as `appdaemon_mqtt_client`, so if two AppDaemon instances use the same broker, the broker keeps disconnecting one of them.
3. `core-mosquitto` if you use the Mosquitto broker app. Otherwise, the host of your MQTT broker without the port (e.g. 192.168.1.10).
4. The user and password of your MQTT broker.
5. Add `mqtt_password: <your password>` to `secrets.yaml`, next to `appdaemon.yaml` (or to the file set in `secrets:`, if your `appdaemon.yaml` has that line). You can also write the password here directly.
6. Optional. By default, AppDaemon subscribes to every MQTT topic (`#`) and receives every message in the broker, even though ControllerX only needs the topics of your controllers. With `NONE`, ControllerX subscribes to just those topics. Leave it out if other AppDaemon apps of yours listen to MQTT topics without subscribing to them.

Then restart the AppDaemon app.
