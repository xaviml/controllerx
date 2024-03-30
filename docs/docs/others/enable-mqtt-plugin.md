---
title: Enable MQTT Plugin
layout: page
---

If we want to use the `mqtt` integration or the `listen_to: mqtt` from `z2m` integration as well as the `Z2MLightController`, we will need to activate the MQTT Plugin on the AppDaemon configuration (normally located in `/addon_configs/a0d7b954_appdaemon/appdaemon.yaml`). We will need the add the following highlighted section in that file:

```yaml hl_lines="12 13 14 15 16 17"
---
secrets: /homeassistant/secrets.yaml
appdaemon:
  latitude: X.XXXXXXX
  longitude: X.XXXXXXX
  elevation: XXXX
  time_zone: XXXXXXXX
  missing_app_warnings: 0 # (1)
  app_dir: /homeassistant/appdaemon/apps
  plugins:
    HASS:
      type: hass
    MQTT:
      type: mqtt
      namespace: mqtt # This is important
      client_host: host # (2)
      client_user: XXXXX # (3)
      client_password: XXXXX
http:
  url: http://127.0.0.1:5050
admin:
api:
hadashboard:
```

1. Extra tip: you can add `missing_app_warnings` if you don't want any warning spam from ControllerX when starting AppDaemon.
2. This is the host without indicating the port (e.g. 192.168.1.10).
3. You should be able to get user and password from MQTT broker.

Then you can just restart the AppDaemon addon/server.
