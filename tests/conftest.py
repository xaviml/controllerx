import asyncio
from asyncio import Task
from typing import Any, Callable

import appdaemon.plugins.hass.hassapi as hass
import appdaemon.plugins.mqtt.mqttapi as mqtt
import pytest
from appdaemon.adapi import ADAPI
from cx_core import Controller
from pytest import MonkeyPatch

from tests.test_utils import fake_fn


async def fake_run_in(
    self: Controller, fn: Callable[..., Any], delay: float, **kwargs: Any
) -> "Task[None]":
    async def inner() -> None:
        await asyncio.sleep(delay)
        await fn(kwargs)

    task = asyncio.create_task(inner())
    return task


async def fake_cancel_timer(self: Controller, task: "Task[None]") -> bool:
    return task.cancel()


@pytest.fixture(autouse=True)
def hass_mock(monkeypatch: MonkeyPatch) -> None:
    """
    Fixture for set up the tests, mocking appdaemon functions
    """

    monkeypatch.setattr(hass.Hass, "__init__", fake_fn())
    monkeypatch.setattr(hass.Hass, "listen_event", fake_fn(async_=True))
    monkeypatch.setattr(mqtt.Mqtt, "listen_event", fake_fn(async_=True))
    monkeypatch.setattr(hass.Hass, "listen_state", fake_fn(async_=True))
    monkeypatch.setattr(hass.Hass, "log", fake_fn())
    monkeypatch.setattr(ADAPI, "call_service", fake_fn(async_=True))
    monkeypatch.setattr(hass.Hass, "get_ad_version", fake_fn(to_return="4.0.0"))
    monkeypatch.setattr(hass.Hass, "run_in", fake_run_in)
    monkeypatch.setattr(hass.Hass, "cancel_timer", fake_cancel_timer)
