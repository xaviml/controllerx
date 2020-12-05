---
layout: page
title: Installation
---

# AppDaemon installation

Before installing ControllerX, we will need to install AppDaemon first. For this, you can follow the [official documentation](https://appdaemon.readthedocs.io/en/latest/INSTALL.html) for it. I personally recommend to install the `AppDaemon 4` addon from the `Add-on store`. Once the addon is install, you can run it and it will set up everything for you. It will create a folder in `/config/appdaemon` with the needed structure for AppDaemon to run.

_You can read [here](/controllerx/others/run-appdaemon) what's AppDaemon and why is needed._

# ControllerX installation

Once you have AppDaemon up and running (check the logs), you can proceed to install ControllerX either manually or through HACS. It is important to have AppDaemon up and running before installing ControllerX.

#### HACS

The easiest way to add this to your Home Assistant installation is using HACS with `Enable AppDaemon apps discovery & tracking` checked. If you don't have it enabled, go to `Configuration > Integrations > HACS (Options)`. You will find ControllerX in the `Automation` section on HACS. Once installed, restart AppDaemon addon/server and go to the [configuration](configuration) page.

#### Manual

Download the [latest version](https://github.com/xaviml/controllerx/releases/latest/download/controllerx.zip), and then place the `controllerx` folder in your machine `/config/appdaemon/apps/controllerx`. The `controllerx.py` needs to be in `/config/appdaemon/apps/controllerx/controllerx.py`. Once copied, restart AppDaemon addon/server and go to the [configuration](configuration) page.

## What's next?

# [Configuration](configuration)
