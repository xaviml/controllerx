# Tasmota Button

![Tasmota Button](<https://xaviml.github.io/controllerx/assets/controllers/TasmotaButton.jpeg>)

- **Manufacturer:** Tasmota
- **Device ID:** `TasmotaButton`
- **Controller types:** [Light](<#light>) (`TasmotaButtonLightController`), [Zigbee2MQTT Light](<#zigbee2mqtt-light>) (`TasmotaButtonZ2MLightController`), [Switch](<#switch>) (`TasmotaButtonSwitchController`), [Cover](<#cover>) (`TasmotaButtonCoverController`)
- **Integrations:** [Tasmota](<https://xaviml.github.io/controllerx/start/integrations/tasmota/index.md>) (`tasmota`)

[Build the configuration for this device](<https://xaviml.github.io/controllerx/start/config-builder/index.md?device=TasmotaButton>)

## Light

- **Class:** `TasmotaButtonLightController`
- **Entity parameter:** `light`
- **Default delay:** `350ms`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#light>) |
| --- | --- |
| `TOGGLE`, `SINGLE` | `toggle` |
| `DOUBLE` | `on_min_brightness` |
| `TRIPLE` | `set_half_brightness` |
| `QUAD` | `on_full_brightness` |
| `PENTA` | *No action* |
| `HOLD` | `hold_brightness_toggle` |
| `CLEAR` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaButtonLightController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  light: light.my_entity_id
```

## Zigbee2MQTT Light

- **Class:** `TasmotaButtonZ2MLightController`
- **Entity parameter:** `light`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#zigbee2mqtt-light>) |
| --- | --- |
| `TOGGLE`, `SINGLE` | `toggle` |
| `DOUBLE` | `on_min_brightness` |
| `TRIPLE` | `set_half_brightness` |
| `QUAD` | `on_full_brightness` |
| `PENTA` | *No action* |
| `HOLD` | `hold_brightness_toggle` |
| `CLEAR` | `release` |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaButtonZ2MLightController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  light: my_entity_id
```

## Switch

- **Class:** `TasmotaButtonSwitchController`
- **Entity parameter:** `switch`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#switch>) |
| --- | --- |
| `TOGGLE`, `SINGLE` | `toggle` |
| `DOUBLE` | `on` |
| `TRIPLE` | `off` |
| `QUAD`, `PENTA`, `HOLD`, `CLEAR` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaButtonSwitchController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  switch: switch.my_entity_id
```

## Cover

- **Class:** `TasmotaButtonCoverController`
- **Entity parameter:** `cover`

### Default mapping

Each row shows the events fired by the device for each integration and the [predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) they trigger by default. You can change it with a [custom mapping](<https://xaviml.github.io/controllerx/advanced/index.md>).

| Tasmota | [Predefined action](<https://xaviml.github.io/controllerx/advanced/predefined-actions/index.md#cover>) |
| --- | --- |
| `TOGGLE`, `SINGLE` | `toggle_open` |
| `DOUBLE`, `HOLD` | `close` |
| `TRIPLE`, `QUAD`, `PENTA`, `CLEAR` | *No action* |

### Example configuration

```
example_app:
  module: controllerx
  class: TasmotaButtonCoverController
  integration:
    name: tasmota
    component: MyComponent
  controller: stat/tasmota_device/RESULT
  cover: cover.my_entity_id
```
