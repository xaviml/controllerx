from types import SimpleNamespace

import pytest
from appdaemon.adapi import ADAPI
from appdaemon.plugins.mqtt.mqttapi import Mqtt
from cx_core import integration as integration_module
from cx_core.controller import Controller
from cx_core.integration.mqtt import MQTTIntegration
from pytest_mock.plugin import MockerFixture


def test_get_integrations(fake_controller: Controller) -> None:
    integrations = integration_module.get_integrations(fake_controller, {})
    inteagration_names = {i.name for i in integrations}
    assert inteagration_names == {
        "z2m",
        "zha",
        "deconz",
        "state",
        "mqtt",
        "lutron_caseta",
        "homematic",
        "shelly",
        "shellyforhass",
        "event",
        "tasmota",
    }


@pytest.mark.parametrize(
    "client_topics, topic, expected_subscribe",
    [
        (["#"], "zigbee2mqtt/controller", False),
        (["zigbee2mqtt/#"], "zigbee2mqtt/controller", False),
        (["zigbee2mqtt/+"], "zigbee2mqtt/controller", False),
        (["zigbee2mqtt/controller"], "zigbee2mqtt/controller", False),
        ([], "zigbee2mqtt/controller", True),
        (["zigbee2mqtt/other"], "zigbee2mqtt/controller", True),
        (["tasmota/#"], "zigbee2mqtt/controller", True),
        (None, "zigbee2mqtt/controller", False),
    ],
)
async def test_listen_mqtt_topic(
    fake_controller: Controller,
    mocker: MockerFixture,
    client_topics: list[str] | None,
    topic: str,
    expected_subscribe: bool,
) -> None:
    plugin = (
        None
        if client_topics is None
        else SimpleNamespace(config=SimpleNamespace(client_topics=client_topics))
    )
    ad = mocker.MagicMock()
    ad.plugins.get_plugin_object.return_value = plugin
    fake_controller.AD = ad
    call_service_mock = mocker.patch.object(ADAPI, "call_service")
    listen_event_mock = mocker.patch.object(Mqtt, "listen_event")
    integration = MQTTIntegration(fake_controller, {})

    await integration.listen_mqtt_topic(topic, integration.event_callback)

    ad.plugins.get_plugin_object.assert_called_once_with("mqtt")
    if expected_subscribe:
        call_service_mock.assert_called_once_with(
            fake_controller, "mqtt/subscribe", topic=topic, namespace="mqtt"
        )
    else:
        call_service_mock.assert_not_called()
    listen_event_mock.assert_called_once_with(
        fake_controller, integration.event_callback, topic=topic, namespace="mqtt"
    )


async def test_listen_mqtt_topic_without_appdaemon(
    fake_controller: Controller, mocker: MockerFixture
) -> None:
    call_service_mock = mocker.patch.object(ADAPI, "call_service")
    listen_event_mock = mocker.patch.object(Mqtt, "listen_event")
    integration = MQTTIntegration(fake_controller, {})

    await integration.listen_mqtt_topic("topic", integration.event_callback)

    call_service_mock.assert_not_called()
    listen_event_mock.assert_called_once()
