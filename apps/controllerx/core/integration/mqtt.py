from typing import Optional

from appdaemon.plugins.mqtt.mqttapi import Mqtt  # type: ignore

from const import TypeActionsMapping
from core.integration import Integration

STATE_HA = "ha"
STATE_MQTT = "mqtt"


class MQTTIntegration(Integration):
    def get_name(self) -> str:
        return "mqtt"

    def get_actions_mapping(self) -> Optional[TypeActionsMapping]:
        return self.controller.get_z2m_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        Mqtt.listen_event(
            self.controller, self.event_callback, topic=controller_id, namespace="mqtt",
        )

    async def event_callback(self, event_name: str, data: dict, kwargs: dict) -> None:
        self.controller.log(f"MQTT data event: {data}", level="DEBUG")
        if "payload" in data:
            await self.controller.handle_action(data["payload"])
