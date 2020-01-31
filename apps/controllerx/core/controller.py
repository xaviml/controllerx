###############################################################
###############################################################
###  CORE CLASSES                                           ###
###                                                         ###
###  All controllers must extend from Controller.           ###
###############################################################
###############################################################

try:
    import hassapi as hass
except:
    import appdaemon.plugins.hass.hassapi as hass
import abc
import time
from collections import defaultdict
from core import integration as integration_module


DEFAULT_DELAY = 350  # In milliseconds
DEFAULT_ACTION_DELTA = 300  # In milliseconds


def action(method):
    async def _action_impl(self, *args, **kwargs):
        continue_call = await self.before_action(method.__name__, *args, **kwargs)
        if continue_call:
            await method(self, *args, **kwargs)

    return _action_impl


class Controller(hass.Hass, abc.ABC):
    """
    This is the parent Controller, all controllers must extend from this class.
    It is mandatory to implement `get_z2m_actions_mapping` to map the controller 
    actions to the internal functions.
    """

    action_times = defaultdict(lambda: 0)

    def initialize(self):
        self.check_ad_version()

        # Get arguments
        self.controllers_ids = self.get_list(self.args["controller"])
        integration = self.get_integration(self.args["integration"])
        self.actions_mapping = self.get_actions_mapping(integration)
        included_actions = self.get_list(
            self.args.get("actions", list(self.actions_mapping.keys()))
        )
        self.action_delta = self.args.get("action_delta", DEFAULT_ACTION_DELTA)

        # Filter the actions
        self.actions_mapping = {
            key: value
            for key, value in self.actions_mapping.items()
            if key in included_actions
        }

        for controller_id in self.controllers_ids:
            integration.listen_changes(controller_id)

    def get_option(self, value, options):
        if value in options:
            return value
        else:
            raise ValueError(f"{value} is not an option. The options are {options}")

    def get_integration(self, integration):
        integrations = integration_module.get_integrations(self)
        integration_argument = self.get_option(
            integration, [i.name for i in integrations]
        )
        return next(i for i in integrations if i.name == integration_argument)

    def check_ad_version(self):
        ad_version = self.get_ad_version()
        major, minor, patch = ad_version.split(".")
        if int(major) < 4:
            raise ValueError("Please upgrade to AppDaemon 4.x")

    def get_actions_mapping(self, integration):
        actions_mapping = integration.get_actions_mapping()
        if actions_mapping is None:
            raise ValueError(f"This controller does not support {integration.name}.")
        return actions_mapping

    def get_list(self, entities):
        type_ = type(entities)
        if type_ == str:
            return entities.replace(" ", "").split(",")
        elif type_ == list:
            return entities

    async def handle_action(self, action_key):
        if action_key in self.actions_mapping:
            previous_call_time = self.action_times[action_key]
            now = time.time() * 1000
            self.action_times[action_key] = now
            if now - previous_call_time > self.action_delta:
                self.log(f"Button pressed after: {action_key}", level="DEBUG")
                action, *args = self.get_action(self.actions_mapping[action_key])
                await action(*args)

    async def before_action(self, action, *args, **kwargs):
        """
        Controllers have the option to implement this function, which is called
        everytime before an action is called and it has the check_before_action decorator.
        It should return True if the action shoul be called. Otherwise it should return False.
        """
        return True

    def get_action(self, action_value):
        if type(action_value) == tuple or type(action_value) == list:
            return action_value
        elif callable(action_value):
            return (action_value,)
        else:
            raise ValueError(
                "The action value from the action mapping should be a list or a function"
            )

    def get_z2m_actions_mapping(self):
        """
        Controllers can implement this function. It should return a dict
        with the states that a controller can take and the functions as values.
        This is used for zigbee2mqtt support.
        """
        return None

    def get_deconz_actions_mapping(self):
        """
        Controllers can implement this function. It should return a dict
        with the event id that a controller can take and the functions as values.
        This is used for deCONZ support.
        """
        return None

    def get_zha_actions_mapping(self):
        """
        Controllers can implement this function. It should return a dict
        with the command that a controller can take and the functions as values.
        This is used for ZHA support.
        """
        return None

    async def get_attr_value(self, entity, attribute):
        if "group." in entity:
            entities = await self.get_state(entity, attribute="entity_id")
            entity = entities[0]
        out = await self.get_state(entity, attribute=attribute)
        return out


class ReleaseHoldController(Controller, abc.ABC):
    def initialize(self):
        super().initialize()
        self.on_hold = False
        self.delay = self.args.get("delay", self.default_delay())

    @action
    async def release(self):
        self.on_hold = False

    @action
    async def hold(self, *args):
        self.on_hold = True
        stop = False
        while self.on_hold and not stop:
            stop = await self.hold_loop(*args)
            await self.sleep(self.delay / 1000)

    async def before_action(self, action, *args, **kwargs):
        to_return = not (action == "hold" and self.on_hold)
        return await super().before_action(action, *args, **kwargs) and to_return

    @abc.abstractmethod
    async def hold_loop(self):
        """
        This function is called by the ReleaseHoldController depending on the settings.
        It stops calling the function once release action is called or when this function
        returns True.
        """
        pass

    def default_delay(self):
        """
        This function can be overwritten for each device to indeicate the delay 
        for the specific device, by default it returns the default delay from the app
        """
        return DEFAULT_DELAY
