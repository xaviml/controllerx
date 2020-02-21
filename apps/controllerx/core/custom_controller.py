from core.controller import Controller, action
from core.type.light_controller import LightController
from core.type.media_player_controller import MediaPlayerController
from const import Light, MediaPlayer
import abc


class CustomController(Controller, abc.ABC):
    def get_custom_mapping(self):
        custom_mapping = self.args["mapping"]
        custom_mapping = {
            event: self.parse_action(action) for event, action in custom_mapping.items()
        }
        return custom_mapping

    @abc.abstractmethod
    def parse_action(self, action):
        """
        This function parse the value of the each action from the 'mapping'.
        It should eiter return a value parsed by 'get_type_actions_mapping' or
        a tuple with (function, arg1, arg2, ...).
        """
        pass

    def get_z2m_actions_mapping(self):
        return self.get_custom_mapping()

    def get_deconz_actions_mapping(self):
        return self.get_custom_mapping()

    def get_zha_actions_mapping(self):
        return self.get_custom_mapping()


class CustomLightController(CustomController, LightController):
    def parse_action(self, action):
        return action


class CustomMediaPlayerController(CustomController, MediaPlayerController):
    def parse_action(self, action):
        return action


class CallServiceController(CustomController):
    def parse_action(self, actions):
        services = []
        if type(actions) == dict:
            actions = [actions]
        for action in actions:
            service = action["service"].replace(".", "/")
            data = action.get("data", {})
            services.append((service, data))
        return (self.call_service, services)

    @action
    async def call_service(self, services):
        for service, data in services:
            await super().call_service(service, **data)
