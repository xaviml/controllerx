---
title: Frequently asked questions (FAQ)
description: Answers to the most common ControllerX problems, like configuration not working, lights not stopping when holding and laggy controllers.
hide:
  - navigation
---

#### 1. I placed the configuration in configuration.yaml and it doesn't work

ControllerX depends on AppDaemon, and all the configuration for AppDaemon apps goes into `apps.yaml` in the AppDaemon apps folder (see [Installation](start/installation.md)) and not `/config/configuration.yaml`.

#### 2. I updated ControllerX to a new version and it does not work

If you installed ControllerX manually, the AppDaemon app (or server) needs to be restarted after updating ControllerX. AppDaemon Store restarts the AppDaemon app on its own after an update. The ControllerX app restarts on its own when updated.

#### 3. I properly configured E1744 (symfonisk) with z2m but it doesn't work

The Zigbee2MQTT documentation recommends setting the `debounce` attribute. However, when it is set, the controller does not send an empty state, and its state stays active instead of being removed. This causes problems for ControllerX, so if you want to use this controller, I recommend removing the `debounce` attribute, since ControllerX already handles repeated events by itself.

#### 4. I have a group of lights and it does not work properly

Please read [entity groups](advanced/entity-groups.md) to understand how grouped entities work.

#### 5. Error: "Value for X attribute could not be retrieved from light Y"

This error is shown when the light supports the X attribute (e.g. brightness or color_temp), but the attribute is not in the state attributes of the entity. You can check whether the attribute X is shown in the state attributes in "Developer Tools > States".

#### 6. Light is not turning on to the previous brightness

Zigbee does not support transitions natively for lights, so this depends on the integration you use for your light. By default, ControllerX adds a transition when changing the brightness or color, but not when turning the light on/off. So if this is happening to you, it might be because `add_transition_turn_toggle: true` is set in your controller configuration. These are the issues related to this problem in the different integrations:

- [Zigbee2MQTT](https://github.com/Koenkk/zigbee-herdsman-converters/issues/1073) (FIXED)
- [Hue integration](https://github.com/home-assistant/core/issues/32894) (CLOSED, but not fixed)

#### 7. When holding or rotating the controller (especially the Symfonisk - E1744), it doesn't stop changing the brightness or volume

This is a known issue that cannot be fixed in the code. Controllers with hold-release functionality fire 2 events: one when the holding/rotation starts and another one when it stops rotating or is released. In between, ControllerX periodically calls HA services to update your brightness, volume, etc. (see [how it works](index.md#how-it-works)).

If this happens to you sometimes, it is because the stop/release action has not been received. This can happen because:

- The rotation is too fast, so the controller cannot tell whether it stopped or not.
- The network is overloaded.
- The server cannot handle the requests on time.
- The controller and the light are far away from the coordinator.

However, these are some things you can do to reduce how often this happens:

- If the `release` action is sent at almost the same time as the `hold` one, you can use the [`release_delay` attribute](start/type-configuration.md#light-controller) to delay `release` actions by some time after they are fired. For example: `release_delay: 0.01` (time in seconds).
- If using z2m, change the integration to listen to MQTT directly, so it avoids the HA state machine layer. Read more about it [here](start/integrations/zigbee2mqtt.md).
- If using deCONZ and you just want to dim your lights smoothly, then you can consider using [this AppDaemon app](https://github.com/Burningstone91/Hue_Dimmer_Deconz) from [_@Burningstone91_](https://github.com/Burningstone91). It brightens/dims your lights with deCONZ calls instead of calling HA periodically, which means that deCONZ handles the dimming for you.
- Play around with the `delay` (default is 350ms) and `automatic_steps` (default is 10) attributes. You can read more about them [here](start/type-configuration.md#light-controller). The lower the delay, the more requests are sent to HA. The higher `automatic_steps`, the more steps it takes to get from min to max, and vice versa.
- Add more Zigbee routers to the network.

#### 8. Symfonisk controller (E1744) is not working with Zigbee2MQTT integration

Do you have a configuration that seems to be right, but is not working? The default mapping for E1744 uses the actions of the new (non-legacy) Zigbee2MQTT implementation for this controller, so you will need to [deactivate the legacy mode](https://www.zigbee2mqtt.io/devices/E1744.html#legacy-integration) for this controller in Zigbee2MQTT. If you use the Zigbee2MQTT app, the device-specific configuration is in `/share/zigbee2mqtt/devices.yaml`. Add `legacy: false` to your E1744 controller as shown in the Zigbee2MQTT documentation, and restart Zigbee2MQTT. While you are here, I strongly recommend checking [FAQ #9](#9-symfonisk-controller-e1744-works-but-pretty-laggy) if your controller feels slow.

#### 9. Symfonisk controller (E1744) works, but pretty laggy

If you are using the `sensor` entity as your controller, I recommend changing the configuration to listen to MQTT directly instead of HA. For this, you will need to change your controller configuration (`apps.yaml`) and enable the AppDaemon MQTT plugin. Your new controller configuration will look like this:

```yaml
example_app:
  module: controllerx
  class: E1744MediaPlayerController
  controller: my_z2m_friendly_name # This is the Zigbee2MQTT friendly name
  integration:
    name: z2m
    listen_to: mqtt
  media_player: media_player.my_media_player
```

Notice how we added the `listen_to` attribute and changed the `controller` to the Zigbee2MQTT friendly name. Finally, you will also need to have the [MQTT plugin enabled](others/enable-mqtt-plugin.md).
