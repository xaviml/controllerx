# Tasmota Switch

![Tasmota Switch](<https://xaviml.github.io/controllerx/assets/controllers/TasmotaSwitch.jpeg>)

- **Manufacturer:** Tasmota
- **Device ID:** `TasmotaSwitch`
- **Controller types:** [Light](<#light>) (`TasmotaSwitchLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`TasmotaSwitchZ2MLightController`), [Switch](<#switch>) (`TasmotaSwitchSwitchController`), [Cover](<#cover>) (`TasmotaSwitchCoverController`)
- **Integrations:** [Tasmota](<https://xaviml.github.io/controllerx/start/integrations/tasmota/index.md>) (`tasmota`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TasmotaSwitch>)

## Light

- **Class:** `TasmotaSwitchLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `TOGGLE` | `toggle` |
| `ON` | `on` |
| `OFF` | `off` |
| `HOLD` | `on_min_max_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaSwitchLightController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `TasmotaSwitchZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `TOGGLE` | `toggle` |
| `ON` | `on` |
| `OFF` | `off` |
| `HOLD` | `set_half_brightness` |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaSwitchZ2MLightController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  light: my_entity_id
```

## Switch

- **Class:** `TasmotaSwitchSwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- |
| `TOGGLE` | `toggle` |
| `ON` | `on` |
| `OFF` | `off` |
| `HOLD` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaSwitchSwitchController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  switch: switch.my_entity_id
```

## Cover

- **Class:** `TasmotaSwitchCoverController`
- **Entity parameter:** `cover`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) |
| --- | --- |
| `TOGGLE` | `toggle_open` |
| `ON` | `open` |
| `OFF` | `close` |
| `HOLD` | `toggle_close` |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaSwitchCoverController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  cover: cover.my_entity_id
```
