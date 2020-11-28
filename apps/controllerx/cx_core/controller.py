import abc
import asyncio
import time
from asyncio.futures import Future
from collections import defaultdict
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Counter,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)

import cx_version
from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from appdaemon.plugins.mqtt.mqttapi import Mqtt  # type: ignore
from cx_const import ActionEvent, ActionFunction, TypeAction, TypeActionsMapping
from cx_core import integration as integration_module
from cx_core.integration import EventData, Integration

Service = Tuple[str, Dict]
Services = List[Service]


DEFAULT_DELAY = 350  # In milliseconds
DEFAULT_ACTION_DELTA = 300  # In milliseconds
DEFAULT_MULTIPLE_CLICK_DELAY = 500  # In milliseconds
MULTIPLE_CLICK_TOKEN = "$"

T = TypeVar("T")


def action(method: Callable[..., Awaitable]) -> ActionFunction:
    @wraps(method)
    async def _action_impl(
        controller: "Controller", *args: Any, **kwargs: Dict[Any, Any]
    ):
        continue_call = await controller.before_action(method.__name__, *args, **kwargs)
        if continue_call:
            await method(controller, *args, **kwargs)

    return _action_impl


def run_in(fn: Callable, delay: float, **kwargs) -> Future:
    """
    It runs the function (fn) to running event loop in `delay` seconds.
    This function has been created because the default run_in function
    from AppDaemon does not accept microseconds.
    """

    async def inner() -> None:
        await asyncio.sleep(delay)
        await fn(kwargs)

    task = asyncio.ensure_future(inner())
    return task


class Controller(Hass, Mqtt, abc.ABC):
    """
    This is the parent Controller, all controllers must extend from this class.
    """

    async def initialize(self) -> None:
        self.log(f"🎮 ControllerX {cx_version.__version__}", ascii_encode=False)
        self.check_ad_version()

        # Get arguments
        self.controllers_ids: List[str] = self.get_list(self.args["controller"])
        integration = self.get_integration(self.args["integration"])

        if "mapping" in self.args and "merge_mapping" in self.args:
            raise ValueError("`mapping` and `merge_mapping` cannot be used together")

        custom_mapping: Dict[ActionEvent, str] = self.args.get("mapping", None)
        merge_mapping: Dict[ActionEvent, str] = self.args.get("merge_mapping", None)

        self.actions_key_mapping: TypeActionsMapping = (
            self.get_actions_mapping(integration)
            if custom_mapping is None
            else self.parse_action_mapping(custom_mapping)
        )
        if merge_mapping is not None:
            self.actions_key_mapping.update(self.parse_action_mapping(merge_mapping))

        self.multiple_click_actions = self.get_multiple_click_actions(
            self.actions_key_mapping
        )

        self.type_actions_mapping = self.get_type_actions_mapping()
        if "actions" in self.args and "excluded_actions" in self.args:
            raise ValueError("`actions` and `excluded_actions` cannot be used together")
        included_actions: Set[ActionEvent] = set(
            self.get_list(
                self.args.get("actions", list(self.actions_key_mapping.keys()))
            )
        )
        excluded_actions: Set[ActionEvent] = set(
            self.get_list(self.args.get("excluded_actions", []))
        )
        included_actions = included_actions - excluded_actions
        default_action_delay = {action_key: 0 for action_key in included_actions}
        self.action_delay: Dict[ActionEvent, int] = {
            **default_action_delay,
            **self.args.get("action_delay", {}),
        }
        self.action_delta: int = self.args.get("action_delta", DEFAULT_ACTION_DELTA)
        self.multiple_click_delay: int = self.args.get(
            "multiple_click_delay", DEFAULT_MULTIPLE_CLICK_DELAY
        )
        self.action_times: Dict[str, float] = defaultdict(lambda: 0.0)
        self.multiple_click_action_times: Dict[str, float] = defaultdict(lambda: 0.0)
        self.click_counter: Counter[ActionEvent] = Counter()
        self.action_delay_handles: Dict[ActionEvent, Optional[float]] = defaultdict(
            lambda: None
        )
        self.multiple_click_action_delay_tasks: Dict[
            ActionEvent, Optional[Future]
        ] = defaultdict(lambda: None)

        # Filter the actions
        filter_actions_mapping: TypeActionsMapping = {
            key: value
            for key, value in self.actions_key_mapping.items()
            if key in included_actions
        }

        # Map the actions mapping with the real functions
        self.actions_mapping = {
            k: (self.type_actions_mapping[v] if isinstance(v, str) else v)
            for k, v in filter_actions_mapping.items()
        }

        for controller_id in self.controllers_ids:
            integration.listen_changes(controller_id)

    def get_option(self, value: str, options: List[str]) -> str:
        if value in options:
            return value
        else:
            raise ValueError(f"{value} is not an option. The options are {options}")

    def parse_integration(
        self, integration: Union[str, Dict[str, Any], Any]
    ) -> Dict[str, str]:
        if isinstance(integration, str):
            return {"name": integration}
        elif isinstance(integration, dict):
            if "name" in integration:
                return integration
            else:
                raise ValueError("'name' attribute is mandatory")
        else:
            raise ValueError(
                f"Type {type(integration)} is not supported for `integration` attribute"
            )

    def get_integration(self, integration: Union[str, Dict[str, Any]]) -> Integration:
        parsed_integration = self.parse_integration(integration)
        kwargs = {k: v for k, v in parsed_integration.items() if k != "name"}
        integrations = integration_module.get_integrations(self, kwargs)
        integration_argument = self.get_option(
            parsed_integration["name"], [i.name for i in integrations]
        )
        return next(i for i in integrations if i.name == integration_argument)

    def check_ad_version(self) -> None:
        ad_version = self.get_ad_version()
        major, _, _ = ad_version.split(".")
        if int(major) < 4:
            raise ValueError("Please upgrade to AppDaemon 4.x")

    def get_actions_mapping(self, integration: Integration) -> TypeActionsMapping:
        actions_mapping = integration.get_actions_mapping()
        if actions_mapping is None:
            raise ValueError(f"This controller does not support {integration.name}.")
        return actions_mapping

    def get_list(self, entities: Union[List[str], str]) -> List[str]:
        if isinstance(entities, str):
            return [entities]
        return entities

    def parse_action_mapping(
        self, mapping: Dict[ActionEvent, str]
    ) -> TypeActionsMapping:
        return {event: self.parse_action(action) for event, action in mapping.items()}

    def get_multiple_click_actions(
        self, mapping: TypeActionsMapping
    ) -> Set[ActionEvent]:
        to_return: Set[ActionEvent] = set()
        for key in mapping.keys():
            if not isinstance(key, str) or MULTIPLE_CLICK_TOKEN not in key:
                continue
            splitted = key.split(MULTIPLE_CLICK_TOKEN)
            assert 1 <= len(splitted) <= 2
            action_key, _ = splitted
            try:
                to_return.add(int(action_key))
            except ValueError:
                to_return.add(action_key)
        return to_return

    def format_multiple_click_action(
        self, action_key: ActionEvent, click_count: int
    ) -> str:
        return (
            str(action_key) + MULTIPLE_CLICK_TOKEN + str(click_count)
        )  # e.g. toggle$2

    async def call_service(self, service: str, **attributes) -> None:
        self.log(
            f"🤖 Service: \033[1m{service.replace('/', '.')}\033[0m",
            level="INFO",
            ascii_encode=False,
        )
        for attribute, value in attributes.items():
            if isinstance(value, float):
                value = f"{value:.2f}"
            self.log(f"  - {attribute}: {value}", level="INFO", ascii_encode=False)
        return await Hass.call_service(self, service, **attributes)

    async def handle_action(self, action_key: str) -> None:
        if (
            action_key in self.actions_mapping
            and action_key not in self.multiple_click_actions
        ):
            previous_call_time = self.action_times[action_key]
            now = time.time() * 1000
            self.action_times[action_key] = now
            if now - previous_call_time > self.action_delta:
                await self.call_action(action_key)
        elif action_key in self.multiple_click_actions:
            now = time.time() * 1000
            previous_call_time = self.multiple_click_action_times.get(action_key, now)
            self.multiple_click_action_times[action_key] = now
            if now - previous_call_time > self.multiple_click_delay:
                pass

            previous_task = self.multiple_click_action_delay_tasks[action_key]
            if previous_task is not None:
                previous_task.cancel()

            self.click_counter[action_key] += 1
            click_count = self.click_counter[action_key]

            new_task = run_in(
                self.multiple_click_call_action,
                self.multiple_click_delay / 1000,
                action_key=action_key,
                click_count=click_count,
            )
            self.multiple_click_action_delay_tasks[action_key] = new_task
        else:
            self.log(
                f"🎮 Button event triggered, but not registered: `{action_key}`",
                level="DEBUG",
                ascii_encode=False,
            )

    async def multiple_click_call_action(self, kwargs: Dict[str, Any]) -> None:
        action_key: ActionEvent = kwargs["action_key"]
        click_count: int = kwargs["click_count"]
        self.log(
            f"🎮 {action_key} clicked `{click_count}` time(s)",
            level="DEBUG",
            ascii_encode=False,
        )
        self.click_counter[action_key] = 0
        click_action_key = self.format_multiple_click_action(action_key, click_count)
        if click_action_key in self.actions_mapping:
            await self.call_action(click_action_key)
        elif action_key in self.actions_mapping and click_count == 1:
            await self.call_action(action_key)

    async def call_action(self, action_key: ActionEvent) -> None:
        self.log(
            f"🎮 Button event triggered: `{action_key}`",
            level="INFO",
            ascii_encode=False,
        )
        delay = self.action_delay[action_key]
        if delay > 0:
            handle = self.action_delay_handles[action_key]
            if handle is not None:
                await self.cancel_timer(handle)
            self.log(
                f"🕒 Running `{self.actions_key_mapping[action_key]}` in {delay} seconds",
                level="INFO",
                ascii_encode=False,
            )
            new_handle = await self.run_in(
                self.action_timer_callback, delay, action_key=action_key
            )
            self.action_delay_handles[action_key] = new_handle
        else:
            await self.action_timer_callback({"action_key": action_key})

    async def action_timer_callback(self, kwargs: Dict[str, Any]):
        action_key: ActionEvent = kwargs["action_key"]
        self.action_delay_handles[action_key] = None
        self.log(
            f"🏃 Running `{self.actions_key_mapping[action_key]}` now",
            level="INFO",
            ascii_encode=False,
        )
        action, *args = self.get_action(self.actions_mapping[action_key])
        await action(*args)

    async def before_action(
        self, action: str, *args: str, **kwargs: Dict[Any, Any]
    ) -> bool:
        """
        Controllers have the option to implement this function, which is called
        everytime before an action is called and it has the check_before_action decorator.
        It should return True if the action shoul be called.
        Otherwise it should return False.
        """
        return True

    def get_action(self, action_value: Union[Sequence, Callable]):
        if isinstance(action_value, tuple) or isinstance(action_value, list):
            return action_value
        elif callable(action_value):
            return (action_value,)
        else:
            raise ValueError(
                "The action value from the action mapping should be a list or a function"
            )

    def parse_action(self, action) -> TypeAction:
        if isinstance(action, str):
            return action
        elif isinstance(action, dict) or isinstance(action, list):
            services: Services = []
            if isinstance(action, dict):
                action = [action]
            for act in action:
                service = act["service"].replace(".", "/")
                data = act.get("data", {})
                services.append((service, data))
            return (self.call_services, services)
        else:
            raise ValueError(
                f"{type(action)} is not supported for the mapping value attributes"
            )

    @action
    async def call_services(self, services: Services) -> None:
        for service, data in services:
            await self.call_service(service, **data)

    def get_z2m_actions_mapping(self) -> Optional[TypeActionsMapping]:
        """
        Controllers can implement this function. It should return a dict
        with the states that a controller can take and the functions as values.
        This is used for zigbee2mqtt support.
        """
        return None

    def get_deconz_actions_mapping(self) -> Optional[TypeActionsMapping]:
        """
        Controllers can implement this function. It should return a dict
        with the event id that a controller can take and the functions as values.
        This is used for deCONZ support.
        """
        return None

    def get_zha_actions_mapping(self) -> Optional[TypeActionsMapping]:
        """
        Controllers can implement this function. It should return a dict
        with the command that a controller can take and the functions as values.
        This is used for ZHA support.
        """
        return None

    def get_zha_action(self, data: EventData) -> Optional[str]:
        """
        This method can be override for controllers that do not support
        the standard extraction of the actions on cx_core/integration/zha.py
        """
        return None

    def get_type_actions_mapping(self) -> TypeActionsMapping:
        return {}


class ReleaseHoldController(Controller, abc.ABC):
    DEFAULT_MAX_LOOPS = 50

    async def initialize(self):
        self.on_hold = False
        self.delay = self.args.get("delay", self.default_delay())
        self.max_loops = self.args.get(
            "max_loops", ReleaseHoldController.DEFAULT_MAX_LOOPS
        )
        self.hold_release_toggle: bool = self.args.get("hold_release_toggle", False)
        await super().initialize()

    @action
    async def release(self) -> None:
        self.on_hold = False

    @action
    async def hold(self, *args) -> None:
        loops = 0
        self.on_hold = True
        stop = False
        while self.on_hold and not stop:
            stop = await self.hold_loop(*args)
            # Stop the iteration if we either stop from the hold_loop
            # or we reached the max loop number
            stop = stop or loops >= self.max_loops
            await self.sleep(self.delay / 1000)
            loops += 1
        self.on_hold = False

    async def before_action(self, action: str, *args, **kwargs) -> bool:
        super_before_action = await super().before_action(action, *args, **kwargs)
        to_return = not (action == "hold" and self.on_hold)
        if action == "hold" and self.on_hold and self.hold_release_toggle:
            self.on_hold = False
        return super_before_action and to_return

    @abc.abstractmethod
    async def hold_loop(self, *args) -> bool:
        """
        This function is called by the ReleaseHoldController depending on the settings.
        It stops calling the function once release action is called or when this function
        returns True.
        """
        raise NotImplementedError

    def default_delay(self) -> int:
        """
        This function can be overwritten for each device to indeicate the delay
        for the specific device, by default it returns the default delay from the app
        """
        return DEFAULT_DELAY
