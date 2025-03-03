from typing import Any

from appdaemon.plugins.hass.hassapi import Hass
from cx_core.integration import EventData, Integration


class EventIntegration(Integration):
    name = "event"

    def get_arg(self, arg: str) -> Any:
        try:
            return self.kwargs[arg]
        except KeyError:
            raise ValueError(f"{arg} is a mandatory field for event integration.")

    async def listen_changes(self, controller_id: str) -> None:
        event_type: str = self.get_arg("event_type")
        controller_key: str = self.get_arg("controller_key")
        self.controller.log(
            f"Listening to `{event_type}` events for controller `{controller_key}={controller_id}`"
        )
        await Hass.listen_event(
            self.controller,
            self.event_callback,
            event_type,
            **{controller_key: controller_id},
        )

    async def event_callback(
        self, event_name: str, data: EventData, kwargs: dict[str, Any]
    ) -> None:
        action_template: str = self.get_arg("action_template")
        try:
            action = action_template.format(**data)
        except Exception:
            self.controller.log(
                f"Template `{action_template}` could not be rendered with data={data}",
                level="WARNING",
            )
            return
        await self.controller.handle_action(action)
