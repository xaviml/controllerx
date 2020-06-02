from typing import Optional

from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from appdaemon.plugins.mqtt.mqttapi import Mqtt  # type: ignore

from const import TypeActionsMapping
from core.integration import Integration

STATE_HA = "ha"
STATE_MQTT = "mqtt"


class Z2MIntegration(Integration):
    def get_name(self) -> str:
        return "z2m"

    def get_actions_mapping(self) -> Optional[TypeActionsMapping]:
        return self.controller.get_z2m_actions_mapping()

    def listen_changes(self, controller_id: str) -> None:
        state = self.kwargs.get("state", "ha")
        if state == STATE_HA:
            Hass.listen_state(self.controller, self.state_callback, controller_id)
        elif state == STATE_MQTT:
            Mqtt.listen_event(
                self.controller,
                self.event_callback,
                "MQTT_MESSAGE",
                topic=controller_id,
            )
        else:
            self.controller.log(
                f"Option `{state}` does not exists for `state` attribute. "
                'Options are: ["ha", "mqtt"]',
                level="WARNING",
            )

    async def event_callback(self, event_name: str, data: dict, kwargs: dict) -> None:
        pass

    async def state_callback(
        self, entity: Optional[str], attribute: Optional[str], old, new, kwargs
    ) -> None:
        await self.controller.handle_action(new)
