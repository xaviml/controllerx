import abc
from typing import Dict, List, Tuple, Union

from cx_const import TypeAction, TypeActionsMapping
from cx_core.controller import Controller, action
from cx_core.type.cover_controller import CoverController
from cx_core.type.light_controller import LightController
from cx_core.type.media_player_controller import MediaPlayerController
from cx_core.type.switch_controller import SwitchController


class CustomController(Controller, abc.ABC):
    def get_custom_mapping(self) -> TypeActionsMapping:
        custom_mapping: Dict[Union[str, int], str] = self.args["mapping"]
        return {
            event: self.parse_action(action) for event, action in custom_mapping.items()
        }

    @abc.abstractmethod
    def parse_action(self, action) -> TypeAction:
        """
        This function parse the value of the each action from the 'mapping'.
        It should eiter return a value parsed by 'get_type_actions_mapping' or
        a tuple with (function, arg1, arg2, ...).
        """
        raise NotImplementedError

    def get_z2m_actions_mapping(self) -> TypeActionsMapping:
        return self.get_custom_mapping()

    def get_deconz_actions_mapping(self) -> TypeActionsMapping:
        return self.get_custom_mapping()

    def get_zha_actions_mapping(self) -> TypeActionsMapping:
        return self.get_custom_mapping()


class CustomLightController(CustomController, LightController):
    def parse_action(self, action) -> TypeAction:
        return action


class CustomMediaPlayerController(CustomController, MediaPlayerController):
    def parse_action(self, action) -> TypeAction:
        return action


class CustomSwitchController(CustomController, SwitchController):
    def parse_action(self, action) -> TypeAction:
        return action


class CustomCoverController(CustomController, CoverController):
    def parse_action(self, action) -> TypeAction:
        return action


Service = Tuple[str, Dict]
Services = List[Service]


class CallServiceController(CustomController):
    def parse_action(self, action) -> TypeAction:
        services: Services = []
        if isinstance(action, dict):
            action = [action]
        for act in action:
            service = act["service"].replace(".", "/")
            data = act.get("data", {})
            services.append((service, data))
        return (self.call_services, services)

    @action
    async def call_services(self, services: Services) -> None:
        for service, data in services:
            await super().call_service(service, **data)
