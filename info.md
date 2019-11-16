## Configuration

For IKEA E1524/E1810:

```yaml
nameOfYourInstanceApp:
  module: z2m_ikea_controller
  class: E1810Controller
  sensor: <sensor entity id>
  light: <light or group entity id>
```

For IKEA E1743:

```yaml
nameOfYourInstanceApp:
  module: z2m_ikea_controller
  class: E1743Controller
  sensor: <sensor entity id>
  light: <light or group entity id>
```

_Note: This was tested with both devices and Zigbee2MQTT, but the code does not use any MQTT calls, just Home assistant API._

| key               | optional | type   | default | example                               | description                                                                                                                                                                                               |
| ----------------- | -------- | ------ | ------- | ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `module`          | False    | string | -       | `z2m_ikea_controller`                 | The Python module                                                                                                                                                                                         |
| `class`           | False    | string | -       | `E1810Controller`                     | The Python class                                                                                                                                                                                          |
| `sensor`          | False    | string | -       | `sensor.livingroom_controller_action` | The sensor entity id from HA. Note that for IKEA E1524/E1810 it finishes with "\_action" by default and for IKEA E1743 with "\_click".                                                                    |
| `light`           | False    | string | -       | `light.livingroom`                    | The light you want to control                                                                                                                                                                             |
| `manual_steps`    | True     | int    | 10      |                                       | Number of steps to go from min to max when clicking. If the value is 2 with one click you will set the light to 50% and with another one to 100%.                                                         |
| `automatic_steps` | True     | int    | 20      |                                       | Number of steps to go from min to max when smoothing. If the value is 2 with one click you will set the light to 50% and with another one to 100%.                                                        |
| `delay`           | True     | int    | 150     |                                       | Delay in milliseconds that takes between sending the instructions to the light (for the smooth functionality). Note that the maximum value is 1000 and if leaving to 0, you might get uncommon behaviour. |
