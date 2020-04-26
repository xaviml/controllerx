import abc
from typing import Dict, List, Tuple, Union

from const import TypeAction, TypeActionsMapping
from core.controller import Controller, action
from core.type.light_controller import LightController
from core.type.media_player_controller import MediaPlayerController


class CustomController(Controller, abc.ABC):
    def get_custom_mapping(self) -> TypeActionsMapping:
        custom_mapping: Dict[Union[str, int], str] = self.args["mapping"]
        return {
            event: self.parse_action(action) for event, action in custom_mapping.items()
        }

    @abc.abstractmethod
    def parse_action(self, action: str) -> TypeAction:
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
    def parse_action(self, action):
        return action


class CustomMediaPlayerController(CustomController, MediaPlayerController):
    def parse_action(self, action):
        return action


Service = Tuple[str, Dict]
Services = List[Service]


class CallServiceController(CustomController):
    def parse_action(self, actions) -> TypeAction:
        services: Services = []
        if type(actions) == dict:
            actions = [actions]
        for act in actions:
            service = act["service"].replace(".", "/")
            data = act.get("data", {})
            services.append((service, data))
        return (self.call_services, services)

    @action
    async def call_services(self, services: Services) -> None:
        for service, data in services:
            await super().call_service(service, **data)
