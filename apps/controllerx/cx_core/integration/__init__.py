import abc
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from appdaemon.adapi import ADAPI
from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_const import DefaultActionsMapping
from cx_helper import get_classes
from paho.mqtt.client import topic_matches_sub

if TYPE_CHECKING:
    from cx_core.controller import Controller

EventData = dict[str, Any]
MQTT_NAMESPACE = "mqtt"


class Integration(abc.ABC):
    name: str
    controller: "Controller"
    kwargs: dict[str, Any]

    def __init__(self, controller: "Controller", kwargs: dict[str, Any]):
        self.controller = controller
        self.kwargs = kwargs

    def get_default_actions_mapping(self) -> DefaultActionsMapping | None:
        return None

    @abc.abstractmethod
    async def listen_changes(self, controller_id: str) -> None:
        raise NotImplementedError

    async def listen_mqtt_topic(
        self,
        topic: str,
        callback: Callable[[str, EventData, dict[str, Any]], Awaitable[None]],
    ) -> None:
        await self._subscribe_mqtt_topic(topic)
        await Mqtt.listen_event(  # type: ignore[misc,unused-ignore]
            self.controller, callback, topic=topic, namespace=MQTT_NAMESPACE
        )

    async def _subscribe_mqtt_topic(self, topic: str) -> None:
        """
        `listen_event` filters the messages AppDaemon receives, but it does not
        subscribe to the topic in the broker. AppDaemon subscribes to every
        topic (`#`) by default, so this is only needed when the MQTT plugin
        is configured with a narrower `client_topics` (e.g. `NONE`). Topics
        already covered by a subscription are skipped, so brokers do not
        deliver the same message twice for overlapping subscriptions.
        """
        ad = getattr(self.controller, "AD", None)
        if ad is None:
            return
        plugin = ad.plugins.get_plugin_object(MQTT_NAMESPACE)
        config = getattr(plugin, "config", None)
        client_topics: list[str] | None = getattr(config, "client_topics", None)
        if client_topics is None:
            return
        if any(topic_matches_sub(sub, topic) for sub in client_topics):
            return
        self.controller.log(f"Subscribing to MQTT topic `{topic}`", level="DEBUG")
        await ADAPI.call_service(
            self.controller,
            "mqtt/subscribe",
            topic=topic,
            namespace=MQTT_NAMESPACE,
        )


def get_integrations(
    controller: "Controller", kwargs: dict[str, Any]
) -> list[Integration]:
    integration_classes = get_classes(__file__, __package__, Integration)
    integrations = [cls_(controller, kwargs) for cls_ in integration_classes]
    return integrations
