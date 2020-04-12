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

from appdaemon.utils import sync_wrapper

import version
from core import integration as integration_module
from core.stepper import Stepper

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
    """

    async def initialize(self):
        self.log(f"ControllerX {version.__version__}")
        self.check_ad_version()

        # Get arguments
        self.controllers_ids = self.get_list(self.args["controller"])
        integration = self.get_integration(self.args["integration"])
        self.actions_mapping = self.get_actions_mapping(integration)
        type_actions_mapping = self.get_type_actions_mapping()
        if "actions" in self.args and "excluded_actions" in self.args:
            raise ValueError("`actions` and `excluded_actions` cannot be used together")
        included_actions = set(
            self.get_list(self.args.get("actions", list(self.actions_mapping.keys())))
        )
        excluded_actions = set(self.get_list(self.args.get("excluded_actions", [])))
        included_actions = included_actions - excluded_actions
        default_action_delay = {action_key: 0 for action_key in included_actions}
        self.action_delay = {
            **default_action_delay,
            **self.args.get("action_delay", {}),
        }
        self.action_delta = self.args.get("action_delta", DEFAULT_ACTION_DELTA)
        self.action_times = defaultdict(lambda: 0)
        self.action_delay_handles = defaultdict(lambda: None)

        # Filter the actions
        self.actions_mapping = {
            key: value
            for key, value in self.actions_mapping.items()
            if key in included_actions
        }

        # Map the actions mapping with the real functions
        self.actions_mapping = {
            k: (type_actions_mapping[v] if type(v) == str else v)
            for k, v in self.actions_mapping.items()
        }

        for controller_id in self.controllers_ids:
            integration.listen_changes(controller_id)

    def get_option(self, value, options):
        if value in options:
            return value
        else:
            raise ValueError(f"{value} is not an option. The options are {options}")

    def parse_integration(self, integration):
        type_ = type(integration)
        if type_ == str:
            return {"name": integration}
        elif type_ == dict:
            if "name" in integration:
                return integration
            else:
                raise ValueError("'name' attribute is mandatory")

    def get_integration(self, integration):
        parsed_integration = self.parse_integration(integration)
        kwargs = {k: v for k, v in parsed_integration.items() if k != "name"}
        integrations = integration_module.get_integrations(self, kwargs)
        integration_argument = self.get_option(
            parsed_integration["name"], [i.name for i in integrations]
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
                self.log(f"Button pressed: {action_key}", level="INFO")
                await self.call_action(action_key)

    async def call_action(self, action_key):
        delay = self.action_delay[action_key]
        if delay > 0:
            handle = self.action_delay_handles[action_key]
            if handle is not None:
                await self.cancel_timer(handle)
            self.log(f"Running {action_key} in {delay} seconds", level="INFO")
            new_handle = await self.run_in(
                self.action_timer_callback, delay, action_key=action_key
            )
            self.action_delay_handles[action_key] = new_handle
        else:
            await self.action_timer_callback({"action_key": action_key})

    async def action_timer_callback(self, kwargs):
        action_key = kwargs["action_key"]
        self.action_delay_handles[action_key] = None
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

    def get_type_actions_mapping(self):
        return {}


class TypeController(Controller, abc.ABC):
    @abc.abstractmethod
    def get_domain(self):
        pass

    async def check_domain(self, entity):
        domain = self.get_domain()
        if entity.startswith("group."):
            entities = await self.get_state(entity, attribute="entity_id")
            same_domain = all([elem.startswith(domain + ".") for elem in entities])
            if not same_domain:
                raise ValueError(
                    f"All entities from '{entity}' must be from {domain} domain (e.g. {domain}.bedroom)"
                )
        elif not entity.startswith(domain + "."):
            raise ValueError(
                f"'{entity}' must be from {domain} domain (e.g. {domain}.bedroom)"
            )

    async def get_entity_state(self, entity, attribute=None):
        if entity.startswith("group."):
            entities = await self.get_state(entity, attribute="entity_id")
            entity = entities[0]
        out = await self.get_state(entity, attribute=attribute)
        return out


class ReleaseHoldController(Controller, abc.ABC):
    async def initialize(self):
        self.on_hold = False
        self.delay = self.args.get("delay", self.default_delay())
        await super().initialize()

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
