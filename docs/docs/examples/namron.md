---
title: Namron 4512772 Example
layout: page
---

### Using the Namron 4512772 Wall Switch

The Namron 4512772 has four groups, and with swappable physical buttons it is intended to control one, two, or four buttons.

To make this work with ControllerX, you can use one app per light you want to control.

For example:

```yaml
test_switch:
  module: controllerx
  class: Namron4512772Controller
  integration:
    name: z2m
    listen_to: mqtt
  controller: My_Namron_Lightswitch # The name of the controller in Z2M
  actions: # Ensure that only the buttons you are interested in are configured.
    - on_l1 # l1 - l4 selects the group of buttons
    - off_l1
    - brightness_move_up_l1
    - brightness_move_down_l1
    - brightness_stop_l1
  light: light.my_light_entity
```

#### Setup with two buttons

If the switch is installed with two physical buttons, it is recommended to configure groups 1 and **4**.

```yaml
test_switch_grp1:
  module: controllerx
  class: Namron4512772Controller
  integration:
    name: z2m
    listen_to: mqtt
  controller: My_Namron_Lightswitch
  actions:
    - on_l1
    - off_l1
    - brightness_move_up_l1
    - brightness_move_down_l1
    - brightness_stop_l1
  light: light.my_light_entity

test_switch_grp2:
  module: controllerx
  class: Namron4512772Controller
  integration:
    name: z2m
    listen_to: mqtt
  controller: My_Namron_Lightswitch
  actions:
    - on_l4 # l4 is the other button needed in a two button setup.
    - off_l4
    - brightness_move_up_l4
    - brightness_move_down_l4
    - brightness_stop_l4
  light: light.my_other_light_entity
```
