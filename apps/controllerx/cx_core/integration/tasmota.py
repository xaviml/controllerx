import json
from typing import Any, Optional

from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class TasmotaIntegration(Integration):
    name = "tasmota"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_tasmota_actions_mapping()

    async def listen_changes(self, controller_id: str) -> None:
        component_key = self.kwargs.get("component")
        if component_key is None:
            raise ValueError(
                "`component` attribute is mandatory. "
                "Check example from https://xaviml.github.io/controllerx/start/integrations/tasmota"
            )
        await Mqtt.listen_event(
            self.controller, self.event_callback, topic=controller_id, namespace="mqtt"
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict[str, Any]
    ) -> None:
        self.controller.log(f"MQTT data event: {data}", level="DEBUG")
        component_key: str = self.kwargs["component"]
        payload_key: str = self.kwargs.get("key", "Action")
        if "payload" not in data:
            return
        payload: str = data["payload"]
        # Even though this checks if "compoenent_key" is in the payload
        # (as string, not dictionary), it is preferred for its performance
        if component_key not in payload:
            return
        try:
            action_key = str(json.loads(payload)[component_key][payload_key])
        except json.decoder.JSONDecodeError:
            raise ValueError(
                f"`key` is being used ({payload_key}). "
                f"Following payload is not a valid JSON: {payload}"
            )
        except KeyError:
            raise ValueError(
                "Following payload does not contain "
                f"payload_key=`{payload_key}`: {payload}"
            )
        await self.controller.handle_action(action_key)
