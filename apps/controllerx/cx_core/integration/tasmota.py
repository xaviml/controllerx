import json
from typing import Any, Dict, Optional

from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class TasmotaIntegration(Integration):
    name = "tasmota"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        device_key = self.kwargs.get("device")
        if device_key is not None:
            if "Button" in device_key:
                return self.controller.get_tasmota_button_actions_mapping()
            elif "Switch" in device_key:
                return self.controller.get_tasmota_switch_actions_mapping()
            else:
                raise ValueError(
                    f"Wrong device type assigned: ({device_key}). "
                    f"Should be one of [Button, Switch]. "
                )
        else:
            raise ValueError(
                f"Device type needs to be assigned: ({device_key}). "
                f"It should be one of [Button, Switch]. "
            )

    async def listen_changes(self, controller_id: str) -> None:
        await Mqtt.listen_event(
            self.controller, self.event_callback, topic=controller_id, namespace="mqtt"
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: Dict[str, Any]
    ) -> None:
        self.controller.log(f"MQTT data event: {data}", level="DEBUG")
        device_key = self.kwargs.get("device")
        payload_key = self.kwargs.get("key", "Action")
        if "payload" not in data or device_key is None:
            return
        payload = data["payload"]
        if device_key in payload:
            try:
                action_key = str(json.loads(payload)[device_key][payload_key])
            except json.decoder.JSONDecodeError:
                raise ValueError(
                    f"`key` is being used ({payload_key}). "
                    f"Following payload is not a valid JSON: {payload}"
                )
            except KeyError:
                raise ValueError(
                    f"Following payload does not contain `{payload_key}`: {payload}"
                )
            await self.controller.handle_action(action_key)
