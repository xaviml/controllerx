The `event` integration is meant to be used with any custom Home Assistant event, so it is not tied to a specific integration.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `event` |
| `event_type`\* | The event we are listening to (e.g. `zha_event`). | `-` |
| `controller_key`\* | The attribute of the controller to listen to (e.g. `device_ieee`). | `-` |
| `action_template`\* | The action template that will be built from the event data (e.g. `action_{command}`). | `-` |

*\* Required fields*

### How to extract the `controller` attribute

To find the controller ID for Event, go to `Developer Tools > Events`, subscribe to the event type you are interested in at the bottom of the page and start listening. Then, press any button on the controller and copy the relevant attribute from the `data` object of the event.

For further explanation and examples, check [here](<https://xaviml.github.io/controllerx/advanced/event-integration/index.md>).
