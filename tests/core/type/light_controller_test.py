import pytest

from core import LightController, ReleaseHoldController
from tests.utils import hass_mock
from core.stepper import Stepper
from core.stepper.minmax_stepper import MinMaxStepper
from core.stepper.circular_stepper import CircularStepper


@pytest.fixture
def sut(hass_mock):
    c = LightController()
    c.args = {}
    c.delay = 0
    c.light = {"name": "light"}
    c.on_hold = False
    return c


@pytest.mark.parametrize(
    "light_input, light_output",
    [
        ("light.kitchen", {"name": "light.kitchen", "color_mode": "auto"}),
        (
            {"name": "light.kitchen", "color_mode": "auto"},
            {"name": "light.kitchen", "color_mode": "auto"},
        ),
        ({"name": "light.kitchen"}, {"name": "light.kitchen", "color_mode": "auto"}),
        (
            {"name": "light.kitchen", "color_mode": "color_temp"},
            {"name": "light.kitchen", "color_mode": "color_temp"},
        ),
    ],
)
def test_initialize_and_get_light(sut, mocker, light_input, light_output):
    super_initialize_stub = mocker.patch.object(ReleaseHoldController, "initialize")

    sut.args["light"] = light_input
    sut.initialize()

    super_initialize_stub.assert_called_once()
    assert sut.light == light_output


@pytest.mark.parametrize(
    "attribute_input, color_mode, light_attributes, attribute_expected, throws_error",
    [
        ("color", "auto", ("xy_color",), "xy_color", False),
        ("color", "auto", ("color_temp",), "color_temp", False),
        ("color", "auto", ("color_temp", "xy_color"), "xy_color", False),
        ("brightness", "auto", (), "brightness", False),
        ("brightness", "auto", ("xy_color",), "brightness", False),
        ("color", "color_temp", ("color_temp", "xy_color"), "color_temp", False),
        ("color", "xy_color", ("color_temp", "xy_color"), "xy_color", False),
        ("color", "auto", (), "not_important", True),
    ],
)
@pytest.mark.asyncio
async def test_get_attribute(
    sut,
    monkeypatch,
    attribute_input,
    color_mode,
    light_attributes,
    attribute_expected,
    throws_error,
):
    async def fake_get_entity_state(entity, attribute=None):
        return {"attributes": set(light_attributes)}

    sut.light = {"name": "light", "color_mode": color_mode}
    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)
    # SUT
    if throws_error:
        with pytest.raises(ValueError) as e:
            await sut.get_attribute(attribute_input)
    else:
        output = await sut.get_attribute(attribute_input)

        # Checks
        assert output == attribute_expected


@pytest.mark.parametrize(
    "attribute_input, expected_output",
    [
        ("xy_color", None),
        ("brightness", "return_from_fake_get_entity_state"),
        ("color_temp", "return_from_fake_get_entity_state"),
    ],
)
@pytest.mark.asyncio
async def test_get_value_attribute(sut, monkeypatch, attribute_input, expected_output):
    async def fake_get_entity_state(entity, attribute):
        return "return_from_fake_get_entity_state"

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    # SUT
    output = await sut.get_value_attribute(attribute_input)

    assert output == expected_output


@pytest.mark.parametrize(
    "old, attribute, direction, stepper, light_state, smooth_power_on, expected_stop, expected_value_attribute",
    [
        (
            50,
            LightController.ATTRIBUTE_BRIGHTNESS,
            Stepper.UP,
            MinMaxStepper(1, 255, 254),
            "on",
            False,
            False,
            51,
        ),
        (0, "xy_color", Stepper.UP, CircularStepper(0, 30, 30), "on", False, False, 0,),
        (
            499,
            "color_temp",
            Stepper.UP,
            MinMaxStepper(153, 500, 10),
            "on",
            False,
            True,
            500,
        ),
        (
            0,
            LightController.ATTRIBUTE_BRIGHTNESS,
            Stepper.UP,
            MinMaxStepper(1, 255, 254),
            "off",
            True,
            True,
            1,
        ),
    ],
)
@pytest.mark.asyncio
async def test_change_light_state(
    sut,
    mocker,
    monkeypatch,
    old,
    attribute,
    direction,
    stepper,
    light_state,
    smooth_power_on,
    expected_stop,
    expected_value_attribute,
):
    async def fake_get_entity_state(*args, **kwargs):
        return light_state

    called_service_patch = mocker.patch.object(sut, "call_service")
    sut.smooth_power_on = smooth_power_on
    sut.value_attribute = old
    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    # SUT
    stop = await sut.change_light_state(old, attribute, direction, stepper)

    # Checks
    assert stop == expected_stop
    assert sut.value_attribute == expected_value_attribute
    called_service_patch.assert_called()


@pytest.mark.asyncio
async def test_on(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    attributes = {"test": "test"}
    await sut.on(**attributes)
    called_service_patch.assert_called_once_with(
        "homeassistant/turn_on", entity_id=sut.light["name"], **attributes
    )


@pytest.mark.asyncio
async def test_off(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.off()
    called_service_patch.assert_called_once_with(
        "homeassistant/turn_off", entity_id=sut.light["name"]
    )


@pytest.mark.asyncio
async def test_toggle(sut, mocker):
    called_service_patch = mocker.patch.object(sut, "call_service")
    await sut.toggle()
    called_service_patch.assert_called_once_with(
        "homeassistant/toggle", entity_id=sut.light["name"]
    )


@pytest.mark.parametrize(
    "min_max, fraction, expected_value",
    [
        ((1, 255), 0, 1),
        ((1, 255), 1, 255),
        ((0, 10), 0.5, 5),
        ((0, 100), 0.2, 20),
        ((0, 100), -1, 0),
        ((0, 100), 1.5, 100),
    ],
)
@pytest.mark.asyncio
async def test_set_value(sut, mocker, min_max, fraction, expected_value):
    attribute = "test_attribute"
    on_patch = mocker.patch.object(sut, "on")
    stepper = MinMaxStepper(min_max[0], min_max[1], 1)
    sut.manual_steppers = {attribute: stepper}

    # SUT
    await sut.set_value(attribute, fraction)

    # Checks
    on_patch.assert_called_once_with(**{attribute: expected_value})


@pytest.mark.asyncio
async def test_on_full(sut, mocker):
    attribute = "test_attribute"
    max_ = 10
    on_patch = mocker.patch.object(sut, "on")
    stepper = MinMaxStepper(1, max_, 10)
    sut.manual_steppers = {attribute: stepper}
    await sut.on_full(attribute)
    on_patch.assert_called_once_with(**{attribute: max_})


@pytest.mark.asyncio
async def test_on_min(sut, mocker):
    attribute = "test_attribute"
    min_ = 1
    on_patch = mocker.patch.object(sut, "on")
    stepper = MinMaxStepper(min_, 10, 10)
    sut.manual_steppers = {attribute: stepper}
    await sut.on_min(attribute)
    on_patch.assert_called_once_with(**{attribute: min_})


@pytest.mark.parametrize(
    "attribute_input, direction_input, light_state, smooth_power_on, expected_calls",
    [
        (LightController.ATTRIBUTE_BRIGHTNESS, Stepper.UP, "off", True, 1),
        ("color_temp", Stepper.UP, "off", True, 0),
        ("color_temp", Stepper.UP, "on", True, 1),
    ],
)
@pytest.mark.asyncio
async def test_click(
    sut,
    monkeypatch,
    mocker,
    attribute_input,
    direction_input,
    light_state,
    smooth_power_on,
    expected_calls,
):
    value_attribute = 10

    async def fake_get_entity_state(*args, **kwargs):
        return light_state

    async def fake_get_value_attribute(*args, **kwargs):
        return value_attribute

    async def fake_get_attribute(*args, **kwargs):
        return attribute_input

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)
    monkeypatch.setattr(sut, "get_value_attribute", fake_get_value_attribute)
    monkeypatch.setattr(sut, "get_attribute", fake_get_attribute)
    change_light_state_patch = mocker.patch.object(sut, "change_light_state")
    sut.smooth_power_on = smooth_power_on
    stepper = MinMaxStepper(1, 10, 10)
    sut.manual_steppers = {attribute_input: stepper}

    # SUT
    await sut.click(attribute_input, direction_input)

    # Checks
    assert change_light_state_patch.call_count == expected_calls


@pytest.mark.parametrize(
    "attribute_input, direction_input, previous_direction, light_state, smooth_power_on, expected_calls, expected_direction",
    [
        (
            LightController.ATTRIBUTE_BRIGHTNESS,
            Stepper.UP,
            Stepper.UP,
            "off",
            True,
            1,
            Stepper.UP,
        ),
        ("color_temp", Stepper.UP, Stepper.UP, "off", True, 0, Stepper.UP),
        ("color_temp", Stepper.UP, Stepper.UP, "on", True, 1, Stepper.UP),
        ("color_temp", Stepper.TOGGLE, Stepper.DOWN, "on", True, 1, Stepper.UP),
    ],
)
@pytest.mark.asyncio
async def test_hold(
    sut,
    monkeypatch,
    mocker,
    attribute_input,
    direction_input,
    previous_direction,
    light_state,
    smooth_power_on,
    expected_calls,
    expected_direction,
):
    value_attribute = 10

    async def fake_get_entity_state(*args, **kwargs):
        return light_state

    async def fake_get_value_attribute(*args, **kwargs):
        return value_attribute

    async def fake_get_attribute(*args, **kwargs):
        return attribute_input

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)
    monkeypatch.setattr(sut, "get_value_attribute", fake_get_value_attribute)
    monkeypatch.setattr(sut, "get_attribute", fake_get_attribute)
    sut.smooth_power_on = smooth_power_on
    stepper = MinMaxStepper(1, 10, 10)
    stepper.previous_direction = previous_direction
    sut.automatic_steppers = {attribute_input: stepper}
    super_hold_patch = mocker.patch.object(ReleaseHoldController, "hold")

    # SUT
    await sut.hold(attribute_input, direction_input)

    # Checks
    assert super_hold_patch.call_count == expected_calls
    if expected_calls > 0:
        super_hold_patch.assert_called_with(attribute_input, expected_direction)


@pytest.mark.asyncio
async def test_hold_loop(sut, mocker):
    attribute = "test_attribute"
    direction = Stepper.UP
    sut.value_attribute = 10
    change_light_state_patch = mocker.patch.object(sut, "change_light_state")
    stepper = MinMaxStepper(1, 10, 10)
    sut.automatic_steppers = {attribute: stepper}
    await sut.hold_loop(attribute, direction)
    change_light_state_patch.assert_called_once_with(
        sut.value_attribute, attribute, direction, stepper
    )
