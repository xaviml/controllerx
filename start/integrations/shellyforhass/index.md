This integration ([**`shellyforhass`**](<https://github.com/StyraHem/ShellyForHASS>)) listens to `shellyforhass.click` events. It creates an action like `<action_type>`. It does not have any additional arguments.

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `name`\* | Integration name. | `shellyforhass` |

*\* Required fields*

## How to extract the `controller` attribute

To find the controller ID for Shelly for HASS, go to `Developer Tools > Events`, subscribe to `shellyforhass.click` at the bottom of the page and start listening. Then, press any button on the controller and copy the `entity_id` from the `data` object of the event. You can read more about the event [here](<https://github.com/StyraHem/ShellyForHASS#shellyforhassclick-020>).
