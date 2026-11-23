This integration ([**`homematic`**](<https://www.home-assistant.io/integrations/homematic>)) listens to `homematic.keypress` events. It creates an action like `<action_type>_<channel>`. It does not have any additional arguments.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `homematic` |

*\* Required fields*

## How to extract the `controller` attribute

To find the controller ID for Homematic, go to `Developer Tools > Events`, subscribe to `homematic.keypress` at the bottom of the page and start listening. Then, press any button on the controller and copy the `name` from the `data` object of the event.
