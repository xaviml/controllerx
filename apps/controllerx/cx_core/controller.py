import asyncio
import re
import time
from ast import literal_eval
from asyncio import CancelledError
from asyncio.futures import Future
from collections import defaultdict
from functools import wraps
from typing import (
    Any,
    Awaitable,
    Callable,
    Counter,
    DefaultDict,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
)

import appdaemon.utils as utils
import cx_version
from appdaemon.plugins.hass.hassapi import Hass  # type: ignore
from appdaemon.plugins.mqtt.mqttapi import Mqtt  # type: ignore
from cx_const import (
    ActionEvent,
    ActionFunction,
    CustomActionsMapping,
    DefaultActionsMapping,
    PredefinedActionsMapping,
)
from cx_core import integration as integration_module
from cx_core.action_type import ActionsMapping, parse_actions
from cx_core.action_type.base import ActionType
from cx_core.integration import EventData, Integration

Service = Tuple[str, Dict]
Services = List[Service]


DEFAULT_ACTION_DELTA = 300  # In milliseconds
DEFAULT_MULTIPLE_CLICK_DELAY = 500  # In milliseconds
MULTIPLE_CLICK_TOKEN = "$"

MODE_SINGLE = "single"
MODE_RESTART = "restart"
MODE_QUEUED = "queued"
MODE_PARALLEL = "parallel"

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

    task = asyncio.create_task(inner())
    return task


class Controller(Hass, Mqtt):
    """
    This is the parent Controller, all controllers must extend from this class.
    """

    integration: Integration
    actions_mapping: ActionsMapping
    action_handles: DefaultDict[ActionEvent, Optional["Future[None]"]]
    action_delay_handles: Dict[ActionEvent, Optional[str]]
    multiple_click_actions: Set[ActionEvent]
    action_delay: Dict[ActionEvent, int]
    action_delta: Dict[ActionEvent, int]
    action_times: Dict[str, float]
    multiple_click_action_times: Dict[str, float]
    click_counter: Counter[ActionEvent]
    multiple_click_action_delay_tasks: DefaultDict[
        ActionEvent, Optional["Future[None]"]
    ]
    multiple_click_delay: int

    async def initialize(self) -> None:
        self.log(f"🎮 ControllerX {cx_version.__version__}", ascii_encode=False)
        await self.init()

    async def init(self) -> None:
        controllers_ids: List[str] = self.get_list(self.args["controller"])
        self.integration = self.get_integration(self.args["integration"])

        if "mapping" in self.args and "merge_mapping" in self.args:
            raise ValueError("`mapping` and `merge_mapping` cannot be used together")

        custom_mapping: CustomActionsMapping = self.args.get("mapping", None)
        merge_mapping: CustomActionsMapping = self.args.get("merge_mapping", None)

        if custom_mapping is None:
            default_actions_mapping = self.get_default_actions_mapping(self.integration)
            self.actions_mapping = self.parse_action_mapping(default_actions_mapping)  # type: ignore
        else:
            self.actions_mapping = self.parse_action_mapping(custom_mapping)

        if merge_mapping is not None:
            self.actions_mapping.update(self.parse_action_mapping(merge_mapping))

        # Filter actions with include and exclude
        if "actions" in self.args and "excluded_actions" in self.args:
            raise ValueError("`actions` and `excluded_actions` cannot be used together")
        include: List[ActionEvent] = self.get_list(
            self.args.get("actions", list(self.actions_mapping.keys()))
        )
        exclude: List[ActionEvent] = self.get_list(
            self.args.get("excluded_actions", [])
        )
        self.actions_mapping = self.filter_actions(
            self.actions_mapping, set(include), set(exclude)
        )

        # Action delay
        self.action_delay = self.get_mapping_per_action(
            self.actions_mapping, custom=self.args.get("action_delay"), default=0
        )
        self.action_delay_handles = defaultdict(lambda: None)
        self.action_handles = defaultdict(lambda: None)

        # Action delta
        self.action_delta = self.get_mapping_per_action(
            self.actions_mapping,
            custom=self.args.get("action_delta"),
            default=DEFAULT_ACTION_DELTA,
        )
        self.action_times = defaultdict(lambda: 0.0)

        # Multiple click
        self.multiple_click_actions = self.get_multiple_click_actions(
            self.actions_mapping
        )
        self.multiple_click_delay = self.args.get(
            "multiple_click_delay", DEFAULT_MULTIPLE_CLICK_DELAY
        )
        self.multiple_click_action_times = defaultdict(lambda: 0.0)
        self.click_counter = Counter()
        self.multiple_click_action_delay_tasks = defaultdict(lambda: None)

        # Mode
        self.mode = self.get_mapping_per_action(
            self.actions_mapping, custom=self.args.get("mode"), default=MODE_SINGLE
        )

        # Listen for device changes
        for controller_id in controllers_ids:
            await self.integration.listen_changes(controller_id)

    def filter_actions(
        self,
        actions_mapping: ActionsMapping,
        include: Set[ActionEvent],
        exclude: Set[ActionEvent],
    ):
        allowed_actions = include - exclude
        return {
            key: value
            for key, value in actions_mapping.items()
            if key in allowed_actions
        }

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

    def get_default_actions_mapping(
        self, integration: Integration
    ) -> DefaultActionsMapping:
        actions_mapping = integration.get_default_actions_mapping()
        if actions_mapping is None:
            raise ValueError(f"This controller does not support {integration.name}.")
        return actions_mapping

    def get_list(self, entities: Union[List[T], T]) -> List[T]:
        if isinstance(entities, (list, tuple)):
            return list(entities)
        return [entities]

    def get_mapping_per_action(
        self,
        actions_mapping: ActionsMapping,
        *,
        custom: Optional[Union[T, Dict[ActionEvent, T]]],
        default: T,
    ) -> Dict[ActionEvent, T]:
        if custom is not None and not isinstance(custom, dict):
            default = custom
        mapping = {action: default for action in actions_mapping}
        if custom is not None and isinstance(custom, dict):
            mapping.update(custom)
        return mapping

    def parse_action_mapping(self, mapping: CustomActionsMapping) -> ActionsMapping:
        return {event: parse_actions(self, action) for event, action in mapping.items()}

    def get_multiple_click_actions(self, mapping: ActionsMapping) -> Set[ActionEvent]:
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

    async def _render_template(self, template: str) -> Any:
        result = await self.call_service("template/render", template=template)
        if result is None:
            raise ValueError(f"Template {template} returned None")
        try:
            return literal_eval(result)
        except (SyntaxError, ValueError):
            return result

    _TEMPLATE_RE = re.compile(r"\s*\{\{.*\}\}")

    def contains_templating(self, template: str) -> bool:
        is_template = self._TEMPLATE_RE.search(template) is not None
        if not is_template:
            self.log(f"`{template}` is not recognized as a template", level="DEBUG")
        return is_template

    async def render_value(self, value: Any) -> Any:
        if isinstance(value, str) and self.contains_templating(value):
            return await self._render_template(value)
        else:
            return value

    async def render_attributes(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        new_attributes: Dict[str, Any] = {}
        for key, value in attributes.items():
            new_value = await self.render_value(value)
            if isinstance(value, dict):
                new_value = await self.render_attributes(value)
            new_attributes[key] = new_value
        return new_attributes

    async def call_service(self, service: str, **attributes) -> Optional[Any]:
        service = service.replace(".", "/")
        to_log = ["\n", f"🤖 Service: \033[1m{service.replace('/', '.')}\033[0m"]
        if service != "template/render":
            attributes = await self.render_attributes(attributes)
        for attribute, value in attributes.items():
            if isinstance(value, float):
                value = f"{value:.2f}"
            to_log.append(f"  - {attribute}: {value}")
        self.log("\n".join(to_log), level="INFO", ascii_encode=False)
        return await Hass.call_service(self, service, **attributes)  # type: ignore

    @utils.sync_wrapper
    async def get_state(
        self,
        entity_id: Optional[str] = None,
        attribute: Optional[str] = None,
        default: Any = None,
        copy: bool = True,
        **kwargs,
    ) -> Optional[Any]:
        rendered_entity_id = await self.render_value(entity_id)
        return await super().get_state(rendered_entity_id, attribute, default, copy, **kwargs)  # type: ignore

    async def handle_action(
        self, action_key: str, extra: Optional[EventData] = None
    ) -> None:
        if (
            action_key in self.actions_mapping
            and action_key not in self.multiple_click_actions
        ):
            previous_call_time = self.action_times[action_key]
            now = time.time() * 1000
            self.action_times[action_key] = now
            if now - previous_call_time > self.action_delta[action_key]:
                await self.call_action(action_key, extra=extra)
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
                extra=extra,
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
        extra: EventData = kwargs["extra"]
        click_count: int = kwargs["click_count"]
        self.multiple_click_action_delay_tasks[action_key] = None
        self.log(
            f"🎮 {action_key} clicked `{click_count}` time(s)",
            level="DEBUG",
            ascii_encode=False,
        )
        self.click_counter[action_key] = 0
        click_action_key = self.format_multiple_click_action(action_key, click_count)
        if click_action_key in self.actions_mapping:
            await self.call_action(click_action_key, extra=extra)
        elif action_key in self.actions_mapping and click_count == 1:
            await self.call_action(action_key, extra=extra)

    async def call_action(
        self, action_key: ActionEvent, extra: Optional[EventData] = None
    ) -> None:
        self.log(
            f"🎮 Button event triggered: `{action_key}`",
            level="INFO",
            ascii_encode=False,
        )
        self.log(
            f"Extra:\n{extra}",
            level="DEBUG",
        )
        delay = self.action_delay[action_key]
        if delay > 0:
            handle = self.action_delay_handles[action_key]
            if handle is not None:
                await self.cancel_timer(handle)  # type: ignore
            self.log(
                f"🕒 Running action(s) from `{action_key}` in {delay} seconds",
                level="INFO",
                ascii_encode=False,
            )
            new_handle = await self.run_in(
                self.action_timer_callback, delay, action_key=action_key, extra=extra
            )  # type: ignore
            self.action_delay_handles[action_key] = new_handle
        else:
            await self.action_timer_callback({"action_key": action_key, "extra": extra})

    async def _apply_mode_strategy(self, action_key: ActionEvent) -> bool:
        previous_task = self.action_handles[action_key]
        if previous_task is None:
            return False
        if self.mode[action_key] == MODE_SINGLE:
            self.log(
                f"There is already an action executing for `{action_key}`. "
                "If you want a different behaviour change `mode` parameter, "
                "the default value is `single`.",
                level="WARNING",
            )
            return True
        elif self.mode[action_key] == MODE_RESTART:
            previous_task.cancel()
        elif self.mode[action_key] == MODE_QUEUED:
            await previous_task
        elif self.mode[action_key] == MODE_PARALLEL:
            pass
        else:
            raise ValueError(
                f"`{self.mode[action_key]}` is not a possible value for `mode` parameter."
                "Possible values: `single`, `restart`, `queued` and `parallel`."
            )
        return False

    async def action_timer_callback(self, kwargs: Dict[str, Any]):
        action_key: ActionEvent = kwargs["action_key"]
        extra: EventData = kwargs["extra"]
        self.action_delay_handles[action_key] = None
        skip = await self._apply_mode_strategy(action_key)
        if skip:
            return
        action_types = self.actions_mapping[action_key]
        task = asyncio.create_task(self.call_action_types(action_types, extra))
        self.action_handles[action_key] = task
        try:
            await task
        except CancelledError:
            self.log(
                f"Task(s) from `{action_key}` was/were canceled and executed again",
                level="DEBUG",
            )
        finally:
            self.action_handles[action_key] = None

    async def call_action_types(
        self, action_types: List[ActionType], extra: Optional[EventData] = None
    ) -> None:
        for action_type in action_types:
            self.log(
                f"🏃 Running `{action_type}` now",
                level="INFO",
                ascii_encode=False,
            )
            await action_type.run(extra=extra)

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

    def get_z2m_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        """
        Controllers can implement this function. It should return a dict
        with the states that a controller can take and the functions as values.
        This is used for zigbee2mqtt support.
        """
        return None

    def get_deconz_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        """
        Controllers can implement this function. It should return a dict
        with the event id that a controller can take and the functions as values.
        This is used for deCONZ support.
        """
        return None

    def get_zha_actions_mapping(self) -> Optional[DefaultActionsMapping]:
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

    def get_lutron_caseta_actions_mapping(self) -> Optional[DefaultActionsMapping]:
        """
        Controllers can implement this function. It should return a dict
        with the command that a controller can take and the functions as values.
        This is used for Lutron support.
        """
        return None

    def get_predefined_actions_mapping(self) -> PredefinedActionsMapping:
        return {}
