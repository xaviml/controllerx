---
layout: page
title: Frequently asked questions (FAQ)
---

#### 1. I placed the configuration in configuration.yaml and it doesn't work

ControllerX depends on AppDaemon and all the configuration for AppDaemon apps goes to `/config/appdaemon/apps/apps.yaml` and not `/config/configuration.yaml`.

#### 2. I updated ControllerX to a new version and it does not work

When updating ControllerX, the AppDaemon server (or addon) needs to be restarted.

#### 3. I properly configured E1744 (symfonisk) with z2m but it doesn't work

From the zigbee2mqtt documentation is recommended to set the `debounce` attribute. However, when set it does not send an empty state and the state of the controller stays active instead of being removed. This causes problems to ControllerX, so if you want to use this controller, I recommend to remove the `debounce` attribute since ControllerX handles repeated events by itself already.

#### 4. I have a group of lights and it does not work properly

Please see [here](/controllerx/advanced/entity-groups) to understand how grouped entities work.

#### 5. Error: "Value for X attribute could not be retrieved from light Y"

This error is shown when the light has support for the X attribute (e.g. brightness or color_temp) and the attribute is not in the state attribute of the entity. You can check whether the attribute X is shown in the state attributes from the "Developer Tools > States".

#### 6. Light is not turning on to the previous brightness

Zigbee does not support transition natively to lights, so this attribute depends on the integration you have installed for your light. ControllerX by default adds transition when changing brightness or color, but not when turning on/off the light. So if this is happening to you it might be because `add_transition_turn_toggle: true` is added in your controller configuration. These are the issues created related to this problem on the different integrations:

- [Zigbee2MQTT](https://github.com/Koenkk/zigbee-herdsman-converters/issues/1073) (FIXED)
- [Hue integration](https://github.com/home-assistant/core/issues/32894) (OPEN)

#### 7. When holding or rotating the controller (especially the Symfonisk - E1744), it doesn't stop changing the brightness or volume

This is a known issue that cannot be fixed in the code. Controllers with holding-release functionality fire 2 events, one when the holding/rotation starts and another when it stops rotating or is released. What ControllerX does for you is send periodically requests to HA via call services to update your brightness, volume, etc.

This is probably happenning to you sometimes and is because the stop/release action has not been fired. This can happen due to:

- A rotation is too fast and confusing to know if it stopped or not.
- The network is overloaded.
- The server cannot handle the requests on time.
- The controller and the light are far distanced from the coordinator.

However, these are some actions you can take to overcome this problem and reduce the number of times that this happens:

- If using z2m, change the integration to listen MQTT directly, this way it will avoid the HA state machine layer. Read more about in [here](/controllerx/others/integrations#zigbee2mqtt).
- If using deCONZ and you just want to dim your lights smoothly, then you can consider using [this AppDaemon app](https://github.com/Burningstone91/Hue_Dimmer_Deconz) from [_@Burningstone91_](https://github.com/Burningstone91). It brightens/dims your lights with a deCONZ calls instead of calling HA periodically, this means that deCONZ would handle the dimming for you.
- Play around with delay (default is 350ms) and automatic_steps (default is 10) attributes. You can read more about them in [here](/controllerx/start/type-configuration#light-controller). The lower the delay is, the more requests will go to HA. The more automatic_steps, the more steps it will take to get from min to max, and vice versa.
- Add more Zigbee routers to the network.

#### 8. Symfonisk controller (E1744) is not working with Zigbee2MQTT integration

Do you have a configuration that seems to be right, but is not working? Well, the default mapping for E1744 has the actions of the new implementation in Zigbee2MQTT for this controller. For this, you will need to [deactivate the legacy mode](https://www.zigbee2mqtt.io/devices/E1744.html#legacy-integration) for this controller in Zigbee2MQTT. If you have the Zigbee2MQTT addon, you will have a file in `/share/zigbee2mqtt/devices.yaml` with the device-specific configuration. You will need to add `legacy: false` to your E1744 controller as shown in the Zigbee2MQTT documentation. With this the problem will be solved once Zigbee2MQTT is restarted. While I have you here reading this, I strongly recommend to you to check the FAQ#9 if you are having slowness issues with your controller.

#### 9. Symfonisk controller (E1744) works, but pretty laggy

If you are using the `sensor` entity as your controller, then I recommend you to change this configuration to listen from MQTT directly instead of HA. For this, you will need to change your controller configuration (`apps.yaml`) and your AppDaemon configuration (`appdaemon.yaml`). Your new controller configurtion will look like this:

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

Notice how we added the `listen_to` attribute and change the `controller` to the Zigbee2MQTT friendly name. Then, you will also need to add the MQTT broker and the credentials in the `appdaemon.yaml` as described in the [MQTT section](/controllerx/others/integrations#mqtt) from the integrations page. Then you can just restart the AppDaemon addon/server.
