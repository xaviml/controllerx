from typing import Optional

from appdaemon.plugins.mqtt.mqttapi import Mqtt  # type: ignore
from cx_const import DefaultActionsMapping
from cx_core.integration import EventData, Integration


class MQTTIntegration(Integration):
    name = "mqtt"

    def get_default_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        return self.controller.get_z2m_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        Mqtt.listen_event(
            self.controller, self.event_callback, topic=controller_id, namespace="mqtt"
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict
    ) -> None:
        self.controller.log(f"MQTT data event: {data}", level="DEBUG")
        if "payload" in data:
            await self.controller.handle_action(data["payload"])
