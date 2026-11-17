This integration (**`lutron_caseta`**) listens to `lutron_caseta_button_event` events. It creates an action like `button_<number>_<action type>`. It does not have any additional arguments.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `lutron_caseta` |

*\* Required fields*

## How to extract the `controller` attribute

To find the controller ID for Lutron Caséta, go to `Developer Tools > Events`, subscribe to `lutron_caseta_button_event` at the bottom of the page and start listening. Then, press any button on the controller and copy the `serial` from the `data` object of the event.
