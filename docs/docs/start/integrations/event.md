---
title: Event
layout: page
---

The `event` integration is meant to be used for a custom event and it is not attached to any type of integration.

## Parameters

| Parameter           | Description                                                                           | Default |
| ------------------- | ------------------------------------------------------------------------------------- | ------- |
| `name`\*            | Integration name.                                                                     | `event` |
| `event_type`\*      | The event we are listening to (e.g. `zha_event`).                                     | `-`     |
| `controller_key`\*  | The attribute of the controller to listen to (e.g. `device_ieee`).                    | `-`     |
| `action_template`\* | The action template that will be built from the event data (e.g. `action_{command}`). | `-`     |

_\* Required fields_

### How to extract the `controller` attribute

To extract the controller ID for Event, you can go to `Developer Tools > Events` then down the bottom you can subscribe for the event type you are interested in and start listening. Then, press any button and you will see the event of the button, you will need to copy the relevant attribute inside the `data` object.

For further explanation and example, please check [here](/controllerx/advanced/event-integration).
