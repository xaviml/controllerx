---
title: Installation
description: Install ControllerX in Home Assistant with the ControllerX app (recommended) or manually in the AppDaemon app, and migrate from HACS.
---

# Installation

ControllerX is an [AppDaemon](../others/run-appdaemon.md) app, so it needs AppDaemon to run. There are two ways to install it in Home Assistant:

- [ControllerX app](#controllerx-app-recommended) (recommended): an app with its own AppDaemon instance and ControllerX preinstalled. ControllerX updates like any other app.
- [Manual installation](#manual-installation): ControllerX copied into the AppDaemon app. Use this if you already run other AppDaemon apps.

If you installed ControllerX through HACS, see [Migrating from HACS](#migrating-from-hacs).

## ControllerX app (recommended)

The ControllerX app runs its own AppDaemon instance with ControllerX preinstalled. Each app update brings the new ControllerX version.

!!! info
    The app's AppDaemon instance is meant only for ControllerX. If you already use the AppDaemon app for other apps, [install ControllerX manually](#manual-installation) in it instead, so you keep a single AppDaemon instance.

1. Add the ControllerX app repository to Home Assistant:

    [![Add repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fxaviml%2Fcontrollerx-app)

    Or go to **Settings → Apps → App store**, select **Repositories** in the top-right menu, and add `https://github.com/xaviml/controllerx-app`.

2. Install the **ControllerX** app and start it.
3. [Configure your controllers](configuration.md) in `/app_configs/d35634e3_controllerx/apps/apps.yaml`, for example with the Studio Code Server or Samba share apps. The app creates this file with a commented example on its first start. AppDaemon picks up changes to it without a restart.

The app keeps all its files in `/app_configs/d35634e3_controllerx/`:

```text
/app_configs/d35634e3_controllerx/
├── appdaemon.yaml      AppDaemon configuration (e.g. to enable the MQTT plugin)
├── secrets.yaml        Optional, for `!secret` values
└── apps/
    ├── apps.yaml       Your ControllerX configuration
    └── controllerx/    ControllerX code, replaced on every app start
```

The `d35634e3` prefix is the one you get when adding the repository with the button or URL above. If your folder has a different prefix, look for the one ending in `_controllerx`.

To update ControllerX, update the app from **Settings → Apps**. Your files aren't changed by updates.

### Moving your configuration to the app

If ControllerX runs in the AppDaemon app today, move its configuration to the ControllerX app. The commands below run in the **Terminal & SSH** app. Set `OLD` to the folder that has your `apps.yaml`:

- `/homeassistant/appdaemon/apps` if you installed ControllerX through HACS (some tools show it as `/config/appdaemon/apps`).
- `/app_configs/a0d7b954_appdaemon/apps` if you installed it manually in the AppDaemon app's default folder.

1. Install and start the ControllerX app once, so it creates its folder.
2. Copy your apps:

    ```bash
    OLD=/homeassistant/appdaemon/apps
    cp "$OLD/apps.yaml" /app_configs/d35634e3_controllerx/apps/apps.yaml
    ```

    If the file also has apps other than ControllerX, remove them from the copy; they stay in the AppDaemon app. Don't copy the `controllerx` folder, the app brings its own.

3. If you use the [MQTT plugin](../others/enable-mqtt-plugin.md), copy its `MQTT:` section from the AppDaemon app's `appdaemon.yaml` into `plugins:` in `/app_configs/d35634e3_controllerx/appdaemon.yaml`, and add `client_id: controllerx` to it, so it doesn't clash with the AppDaemon app on the MQTT broker (see [Enable MQTT plugin](../others/enable-mqtt-plugin.md)). If you copy other settings too, **leave out the `app_dir` line**: the app always uses its own `apps` folder. Also leave out `secrets: /homeassistant/secrets.yaml`, since the app can't read the Home Assistant configuration folder.
4. If your configuration uses `!secret`, copy those secrets into `/app_configs/d35634e3_controllerx/secrets.yaml`.
5. Remove ControllerX from the AppDaemon app:
    - If you only used AppDaemon for ControllerX, uninstall the AppDaemon app.
    - Otherwise, remove the ControllerX apps from its `apps.yaml`, delete the ControllerX code with `rm -rf "$OLD/controllerx"`, and restart the AppDaemon app.
6. Restart the ControllerX app and check its **Log** tab.

## Manual installation

1. Install the **AppDaemon** app from **Settings → Apps → App store** and start it once. It creates its folder in `/app_configs/a0d7b954_appdaemon/`.
2. Install the **Terminal & SSH** app, open its terminal, and run:

    ```bash
    APPS=/app_configs/a0d7b954_appdaemon/apps; rm -rf "$APPS/controllerx" && mkdir -p "$APPS/controllerx" && curl -fsSL https://github.com/xaviml/controllerx/releases/latest/download/controllerx.zip -o /tmp/controllerx.zip && unzip -oq /tmp/controllerx.zip -d "$APPS/controllerx" && rm /tmp/controllerx.zip
    ```

    This downloads the latest ControllerX release into `/app_configs/a0d7b954_appdaemon/apps/controllerx/`.

3. [Configure your controllers](configuration.md) in `/app_configs/a0d7b954_appdaemon/apps/apps.yaml`.
4. Restart the AppDaemon app.

If you run AppDaemon in some other way, download [controllerx.zip](https://github.com/xaviml/controllerx/releases/latest/download/controllerx.zip) and unzip it into a `controllerx` folder inside your AppDaemon apps folder, so that `controllerx.py` ends up in `<apps folder>/controllerx/controllerx.py`.

### Updating

Run the same command again and restart the AppDaemon app. It only replaces the `controllerx` folder, so your `apps.yaml` stays as it is. To know when there's a new version, you can watch the [ControllerX releases](https://github.com/xaviml/controllerx/releases) on GitHub (**Watch → Custom → Releases**).

## Migrating from HACS

HACS no longer supports AppDaemon apps. ControllerX installed through HACS keeps working, but it won't get updates anymore. HACS installed it in `/homeassistant/appdaemon/apps/controllerx`, next to your `apps.yaml`. Switch to one of the installation methods above:

- **Stay with the AppDaemon app:** you don't need to move anything. Update ControllerX with the [manual installation](#manual-installation) command, using your current folder, and restart the AppDaemon app:

    ```bash
    APPS=/homeassistant/appdaemon/apps; rm -rf "$APPS/controllerx" && mkdir -p "$APPS/controllerx" && curl -fsSL https://github.com/xaviml/controllerx/releases/latest/download/controllerx.zip -o /tmp/controllerx.zip && unzip -oq /tmp/controllerx.zip -d "$APPS/controllerx" && rm /tmp/controllerx.zip
    ```

    Keep the `app_dir: /homeassistant/appdaemon/apps` line in your `appdaemon.yaml`, it's what points AppDaemon to this folder.

- **Switch to the ControllerX app:** follow [Moving your configuration to the app](#moving-your-configuration-to-the-app).

!!! warning
    Keep only one copy of ControllerX running. If the same controller is configured in both the AppDaemon app and the ControllerX app, every button press runs twice (for example, a toggle turns the light on and straight back off).

## Enabling the MQTT plugin (optional)

If you use the Zigbee2MQTT integration, [enable the MQTT plugin](../others/enable-mqtt-plugin.md), since the [Home Assistant sensor listener is deprecated](../others/z2m-ha-sensor-deprecated.md).
