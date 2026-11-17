This integration (**`zha`**) listens to `zha_event` events and builds the action by concatenating the command with its arguments. It does not have any additional arguments.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `zha` |

*\* Required fields*

## How to extract the `controller` attribute

To find the controller ID for ZHA, go to `Developer Tools > Events`, subscribe to `zha_event` at the bottom of the page and start listening. Then, press any button on the controller and copy the `device_ieee` from the `data` object of the event. It looks like `00:67:88:56:06:78:9b:3f`.
