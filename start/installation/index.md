# Installation

ControllerX is an [AppDaemon](<https://xaviml.github.io/controllerx/others/run-appdaemon/index.md>) app, so it needs AppDaemon to run. In Home Assistant you can install it in three ways:

| Option | AppDaemon used | How ControllerX is updated | Best for |
| --- | --- | --- | --- |
| [**ControllerX app**](<#controllerx-app-recommended>) (recommended) | Its own, built in | Update the app from **Settings → Apps** | You only use AppDaemon for ControllerX |
| [**AppDaemon Store + AppDaemon app**](<#appdaemon-store-and-appdaemon-app>) | The AppDaemon app | From the AppDaemon Store UI | You already run, or plan to run, other AppDaemon apps |
| [**Manual**](<#manual-installation>) | The AppDaemon app | Download and copy the new release by hand | Same as above, without installing AppDaemon Store |

> [!TIP]
>
> **Which one should I choose?**
>
> - **New to AppDaemon?** Use the [ControllerX app](<#controllerx-app-recommended>). It's the simplest setup: one app to install, configure and update.
> - **Already using the AppDaemon app for other apps?** Install ControllerX in it with [AppDaemon Store](<#appdaemon-store-and-appdaemon-app>), so you keep a single AppDaemon instance and get a UI to install and update ControllerX and your other AppDaemon apps.
> - **Prefer to manage files yourself?** Follow the [manual installation](<#manual-installation>).

If you installed ControllerX through HACS, see [Migrating from HACS](<#migrating-from-hacs>).

> [!WARNING]
>
> Run only one copy of ControllerX. If the same controller is configured in both the ControllerX app and the AppDaemon app, every button press runs twice (for example, a toggle turns the light on and straight back off).

## ControllerX app (recommended)

The ControllerX app runs its own AppDaemon instance with ControllerX preinstalled. Each app update brings the new ControllerX version.

1. Add the ControllerX app repository to Home Assistant:

   [![Add repository to Home Assistant](<https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg>)](<https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fxaviml%2Fcontrollerx-app>)

   Or go to **Settings → Apps → App store**, select **Repositories** in the top-right menu, and add `https://github.com/xaviml/controllerx-app`.
2. Install the **ControllerX** app and start it.
3. [Configure your controllers](<https://xaviml.github.io/controllerx/start/configuration/index.md>) in `/app_configs/d35634e3_controllerx/apps/apps.yaml`, for example with the Studio Code Server or Samba share apps. The app creates this file with a commented example on its first start. AppDaemon picks up changes to it without a restart, unless **Production mode** is on in the app's **Configuration** tab.

**Updating:** update the app from **Settings → Apps**. Your files aren't changed by updates.

> [!NOTE]
>
> **Where the app keeps its files**
>
> ```
> /app_configs/d35634e3_controllerx/
> ├── secrets.yaml        Optional, for `!secret` values
> └── apps/
>     ├── apps.yaml       Your ControllerX configuration
>     └── controllerx/    ControllerX code, replaced on every app start
> ```
>
> The `d35634e3` prefix is the one you get when adding the repository with the button or URL above. If your folder has a different prefix, look for the one ending in `_controllerx`.

> [!NOTE]
>
> The app's AppDaemon instance is meant only for ControllerX: you can't add other AppDaemon apps to it. If you need other AppDaemon apps, use the [AppDaemon Store](<#appdaemon-store-and-appdaemon-app>) option instead.

## AppDaemon Store and AppDaemon app

[AppDaemon Store](<https://github.com/mietzen/appdaemon-store>) is a community app that installs and updates AppDaemon apps from GitHub through a UI in the Home Assistant sidebar. It installs them into the **AppDaemon** app, which runs them. Use this option when you also run other AppDaemon apps, so all of them share a single AppDaemon instance and are managed from one place.

> [!NOTE]
>
> **Kudos**
>
> Many thanks to [mietzen](<https://github.com/mietzen>) for developing and maintaining AppDaemon Store, which brings back a simple way to install and update AppDaemon apps now that HACS no longer supports them.

1. Install the **AppDaemon** app from **Settings → Apps → App store** and start it once. It creates its folder in `/app_configs/a0d7b954_appdaemon/`.
2. Add the AppDaemon Store repository to Home Assistant:

   [![Add repository to Home Assistant](<https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg>)](<https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fmietzen%2Fhassio-addons>)

   Or go to **Settings → Apps → App store**, select **Repositories** in the top-right menu, and add `https://github.com/mietzen/hassio-addons`.
3. Install the **AppDaemon Store** app, start it, and open **AppDaemon Store** from the sidebar.
4. Add the `xaviml/controllerx` repository. ControllerX is installed in `/app_configs/a0d7b954_appdaemon/apps/controllerx/`.
5. [Configure your controllers](<https://xaviml.github.io/controllerx/start/configuration/index.md>) in `/app_configs/a0d7b954_appdaemon/apps/apps.yaml`.
6. Restart the AppDaemon app.

**Updating:** AppDaemon Store checks for new releases and sends a Home Assistant notification when one is available. Update ControllerX from the AppDaemon Store UI, or enable auto-update for it so new releases are installed on their own. Either way, AppDaemon Store restarts the AppDaemon app for you, so the new version is loaded without any manual step.

## Manual installation

Use this to install ControllerX in the AppDaemon app without AppDaemon Store, or if you run AppDaemon in some other way (e.g. Docker).

1. Install the **AppDaemon** app from **Settings → Apps → App store** and start it once. It creates its folder in `/app_configs/a0d7b954_appdaemon/`.
2. Download [controllerx.zip](<https://github.com/xaviml/controllerx/releases/latest/download/controllerx.zip>) from the latest release and unzip it into a `controllerx` folder in the AppDaemon apps folder, so that you end up with `/app_configs/a0d7b954_appdaemon/apps/controllerx/controllerx.py`. You can copy the files with the Samba share or Studio Code Server apps.
3. [Configure your controllers](<https://xaviml.github.io/controllerx/start/configuration/index.md>) in `/app_configs/a0d7b954_appdaemon/apps/apps.yaml`.
4. Restart the AppDaemon app.

**Updating:** delete the `controllerx` folder, repeat step 2 with the new release, and restart the AppDaemon app. Your `apps.yaml` stays as it is. To know when there's a new version, watch the [ControllerX releases](<https://github.com/xaviml/controllerx/releases>) on GitHub (**Watch → Custom → Releases**).

## Migrating from HACS

HACS no longer supports AppDaemon apps. ControllerX installed through HACS keeps working, but it won't get updates anymore. HACS installed it in `/homeassistant/appdaemon/apps/controllerx`, next to your `apps.yaml`. Move to one of the options above:

- **ControllerX app:** if you only use AppDaemon for ControllerX, follow [Moving to the ControllerX app](<#moving-to-the-controllerx-app>).
- **AppDaemon Store:** if you use other AppDaemon apps, install [AppDaemon Store](<#appdaemon-store-and-appdaemon-app>). Its HACS migration assistant detects the HACS setup and, after you confirm, moves your apps and `apps.yaml` to `/app_configs/a0d7b954_appdaemon/apps` and updates `appdaemon.yaml`. Then add the `xaviml/controllerx` repository so AppDaemon Store manages ControllerX from now on.
- **Manual:** keep your current folder and update ControllerX by replacing `/homeassistant/appdaemon/apps/controllerx` with the [latest release](<#manual-installation>). Keep the `app_dir: /homeassistant/appdaemon/apps` line in your `appdaemon.yaml`; it's what points AppDaemon to this folder.

## Moving to the ControllerX app

If ControllerX runs in the AppDaemon app today (installed through HACS, AppDaemon Store or manually), you can move its configuration to the ControllerX app. Your current `apps.yaml` is in one of these folders:

- `/homeassistant/appdaemon/apps` if you installed ControllerX through HACS (some tools show it as `/config/appdaemon/apps`).
- `/app_configs/a0d7b954_appdaemon/apps` otherwise.
- Install and start the [ControllerX app](<#controllerx-app-recommended>) once, so it creates its folder.
- Copy your `apps.yaml` to `/app_configs/d35634e3_controllerx/apps/apps.yaml`. If it also has apps other than ControllerX, remove them from the copy. Don't copy the `controllerx` folder, the app brings its own.
- If you use the [MQTT plugin](<https://xaviml.github.io/controllerx/others/enable-mqtt-plugin/index.md>), turn on **Enable MQTT** in the app's **Configuration** tab. Don't copy the AppDaemon app's `appdaemon.yaml`: the ControllerX app manages its AppDaemon configuration itself.
- If your configuration uses `!secret`, copy those secrets into `/app_configs/d35634e3_controllerx/secrets.yaml`.
- Remove ControllerX from the AppDaemon app:

  - If you only used AppDaemon for ControllerX, uninstall the AppDaemon app (and AppDaemon Store, if you had it).
  - Otherwise, remove the ControllerX apps from its `apps.yaml`, remove ControllerX from AppDaemon Store or delete the `controllerx` folder, and restart the AppDaemon app.
- Restart the ControllerX app and check its **Log** tab.

## Enabling the MQTT plugin (optional)

If you use the Zigbee2MQTT integration, [enable the MQTT plugin](<https://xaviml.github.io/controllerx/others/enable-mqtt-plugin/index.md>), since the [Home Assistant sensor listener is deprecated](<https://xaviml.github.io/controllerx/others/z2m-ha-sensor-deprecated/index.md>).
