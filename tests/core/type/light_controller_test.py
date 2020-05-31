import pytest

from core import LightController, ReleaseHoldController
from core.feature_support import FeatureSupport
from core.feature_support.light import LightSupport
from core.stepper import Stepper
from core.stepper.circular_stepper import CircularStepper
from core.stepper.minmax_stepper import MinMaxStepper
from tests.test_utils import fake_async_function, hass_mock


@pytest.fixture
def sut(hass_mock, monkeypatch):
    c = LightController()
    c.args = {}
    c.delay = 0
    c.light = {"name": "light"}
    c.on_hold = False

    monkeypatch.setattr(c, "get_entity_state", fake_async_function("0"))
    return c


@pytest.mark.parametrize(
    "light_input, light_output, error_expected",
    [
        ("light.kitchen", {"name": "light.kitchen", "color_mode": "auto"}, False),
        (
            {"name": "light.kitchen", "color_mode": "auto"},
            {"name": "light.kitchen", "color_mode": "auto"},
            False,
        ),
        (
            {"name": "light.kitchen"},
            {"name": "light.kitchen", "color_mode": "auto"},
            False,
        ),
        (
            {"name": "light.kitchen", "color_mode": "color_temp"},
            {"name": "light.kitchen", "color_mode": "color_temp"},
            False,
        ),
        (0.0, None, True),
    ],
)
@pytest.mark.asyncio
async def test_initialize_and_get_light(
    sut, monkeypatch, mocker, light_input, light_output, error_expected
):
    super_initialize_stub = mocker.stub()

    async def fake_super_initialize(self):
        super_initialize_stub()

    monkeypatch.setattr(ReleaseHoldController, "initialize", fake_super_initialize)

    sut.args["light"] = light_input

    # SUT
    if error_expected:
        with pytest.raises(ValueError) as e:
            await sut.initialize()
    else:
        await sut.initialize()

        # Checks
        super_initialize_stub.assert_called_once()
        assert sut.light == light_output


@pytest.mark.parametrize(
    "attribute_input, color_mode, supported_features, attribute_expected, throws_error",
    [
        ("color", "auto", {LightSupport.COLOR}, "xy_color", False),
        ("color", "auto", {LightSupport.COLOR_TEMP}, "color_temp", False),
        (
            "color",
            "auto",
            {LightSupport.COLOR, LightSupport.COLOR_TEMP},
            "xy_color",
            False,
        ),
        ("brightness", "auto", set(), "brightness", False),
        ("brightness", "auto", {LightSupport.COLOR}, "brightness", False),
        (
            "color",
            "color_temp",
            {LightSupport.COLOR, LightSupport.COLOR_TEMP},
            "color_temp",
            False,
        ),
        (
            "color",
            "xy_color",
            {LightSupport.COLOR, LightSupport.COLOR_TEMP},
            "xy_color",
            False,
        ),
        ("color", "auto", set(), "not_important", True),
    ],
)
def test_get_attribute(
    sut,
    monkeypatch,
    attribute_input,
    color_mode,
    supported_features,
    attribute_expected,
    throws_error,
):
    sut.supported_features = LightSupport(FeatureSupport.encode(supported_features))
    sut.light = {"name": "light", "color_mode": color_mode}

    # SUT
    if throws_error:
        with pytest.raises(ValueError) as e:
            sut.get_attribute(attribute_input)
    else:
        output = sut.get_attribute(attribute_input)

        # Checks
        assert output == attribute_expected


@pytest.mark.parametrize(
    "attribute_input, expected_output, error_expected",
    [
        ("xy_color", 0, False),
        ("brightness", 3.0, False),
        ("brightness", "3.0", False),
        ("brightness", "3", False),
        ("brightness", "error", True),
        ("color_temp", 1, False),
        ("xy_color", 0, False),
        ("brightness", None, True),
        ("color_temp", None, True),
        ("not_a_valid_attribute", None, True),
    ],
)
@pytest.mark.asyncio
async def test_get_value_attribute(
    sut, monkeypatch, attribute_input, expected_output, error_expected
):
    async def fake_get_entity_state(entity, attribute):
        return expected_output

    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    # SUT
    if error_expected:
        with pytest.raises(ValueError) as e:
            await sut.get_value_attribute(attribute_input)
    else:
        output = await sut.get_value_attribute(attribute_input)

        # Checks
        assert output == float(expected_output)


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
            0,
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
    sut.manual_steppers = {attribute: stepper}
    sut.automatic_steppers = {attribute: stepper}
    sut.transition = 300
    sut.supported_features = LightSupport(0)
    monkeypatch.setattr(sut, "get_entity_state", fake_get_entity_state)

    # SUT
    stop = await sut.change_light_state(old, attribute, direction, stepper, "hold")

    # Checks
    assert stop == expected_stop
    assert sut.value_attribute == expected_value_attribute
    called_service_patch.assert_called()


@pytest.mark.parametrize(
    "attributes_input, transition_support, turned_toggle, add_transition, add_transition_turn_toggle, attributes_expected",
    [
        ({"test": "test"}, True, True, True, True, {"test": "test", "transition": 0.3}),
        ({"test": "test"}, False, True, True, True, {"test": "test"}),
        (
            {"test": "test", "transition": 0.5},
            True,
            True,
            True,
            True,
            {"test": "test", "transition": 0.5},
        ),
        (
            {"test": "test", "transition": 0.5},
            False,
            True,
            True,
            True,
            {"test": "test"},
        ),
        ({}, True, True, True, True, {"transition": 0.3}),
        ({}, True, True, True, False, {}),
        ({}, True, True, False, True, {}),
        ({}, True, True, False, False, {}),
        ({}, True, False, True, True, {"transition": 0.3}),
        ({}, True, False, True, False, {"transition": 0.3}),
        ({}, True, False, False, True, {}),
        ({}, True, False, False, False, {}),
        ({}, False, True, True, True, {}),
        ({}, False, True, True, False, {}),
        ({}, False, True, False, True, {}),
        ({}, False, True, False, False, {}),
        ({}, False, False, True, True, {}),
        ({}, False, False, True, False, {}),
        ({}, False, False, False, True, {}),
        ({}, False, False, False, False, {}),
    ],
)
@pytest.mark.asyncio
async def test_call_light_service(
    sut,
    mocker,
    attributes_input,
    transition_support,
    turned_toggle,
    add_transition,
    add_transition_turn_toggle,
    attributes_expected,
):
    called_service_patch = mocker.patch.object(sut, "call_service")
    sut.transition = 300
    sut.add_transition = add_transition
    sut.add_transition_turn_toggle = add_transition_turn_toggle
    supported_features = {LightSupport.TRANSITION} if transition_support else set()
    sut.supported_features = LightSupport(FeatureSupport.encode(supported_features))
    await sut.call_light_service(
        "test_service", turned_toggle=turned_toggle, **attributes_input
    )
    called_service_patch.assert_called_once_with(
        "test_service", entity_id=sut.light["name"], **attributes_expected
    )


@pytest.mark.parametrize(
    "light_on, light_state, expected_turned_toggle",
    [(True, any, False), (False, any, True), (None, "on", False), (None, "off", True)],
)
@pytest.mark.asyncio
async def test_on(
    sut, mocker, monkeypatch, light_on, light_state, expected_turned_toggle
):
    monkeypatch.setattr(sut, "call_light_service", fake_async_function())
    mocker.patch.object(sut, "get_entity_state", fake_async_function(light_state))
    call_light_service_patch = mocker.patch.object(sut, "call_light_service")
    attributes = {"test": 0}

    await sut.on(light_on=light_on, **attributes)
    call_light_service_patch.assert_called_once_with(
        "light/turn_on", turned_toggle=expected_turned_toggle, **attributes
    )


@pytest.mark.asyncio
async def test_off(sut, mocker, monkeypatch):
    monkeypatch.setattr(sut, "call_light_service", fake_async_function())
    call_light_service_patch = mocker.patch.object(sut, "call_light_service")
    attributes = {"test": 0}

    await sut.off(**attributes)
    call_light_service_patch.assert_called_once_with(
        "light/turn_off", turned_toggle=True, **attributes
    )


@pytest.mark.asyncio
async def test_toggle(sut, mocker, monkeypatch):
    monkeypatch.setattr(sut, "call_light_service", fake_async_function())
    call_light_service_patch = mocker.patch.object(sut, "call_light_service")
    attributes = {"test": 0}

    await sut.toggle(**attributes)
    call_light_service_patch.assert_called_once_with(
        "light/toggle", turned_toggle=True, **attributes
    )


@pytest.mark.parametrize(
    "stepper_cls, min_max, fraction, expected_calls, expected_value",
    [
        (MinMaxStepper, (1, 255), 0, 1, 1),
        (MinMaxStepper, (1, 255), 1, 1, 255),
        (MinMaxStepper, (0, 10), 0.5, 1, 5),
        (MinMaxStepper, (0, 100), 0.2, 1, 20),
        (MinMaxStepper, (0, 100), -1, 1, 0),
        (MinMaxStepper, (0, 100), 1.5, 1, 100),
        (CircularStepper, (0, 100), 0, 0, None),
    ],
)
@pytest.mark.asyncio
async def test_set_value(
    sut, mocker, stepper_cls, min_max, fraction, expected_calls, expected_value
):
    attribute = "test_attribute"
    on_patch = mocker.patch.object(sut, "on")
    stepper = stepper_cls(min_max[0], min_max[1], 1)
    sut.automatic_steppers = {attribute: stepper}

    # SUT
    await sut.set_value(attribute, fraction, light_on=False)

    # Checks
    assert on_patch.call_count == expected_calls
    if expected_calls > 0:
        on_patch.assert_called_with(light_on=False, **{attribute: expected_value})


@pytest.mark.asyncio
async def test_on_full(sut, mocker):
    attribute = "test_attribute"
    max_ = 10
    on_patch = mocker.patch.object(sut, "on")
    stepper = MinMaxStepper(1, max_, 10)
    sut.automatic_steppers = {attribute: stepper}

    # SUT
    await sut.on_full(attribute, light_on=False)

    # Checks
    on_patch.assert_called_once_with(light_on=False, **{attribute: max_})


@pytest.mark.asyncio
async def test_on_min(sut, mocker):
    attribute = "test_attribute"
    min_ = 1
    on_patch = mocker.patch.object(sut, "on")
    stepper = MinMaxStepper(min_, 10, 10)
    sut.automatic_steppers = {attribute: stepper}

    # SUT
    await sut.on_min(attribute, light_on=False)

    # Checks
    on_patch.assert_called_once_with(light_on=False, **{attribute: min_})


@pytest.mark.parametrize(
    "max_brightness, color_attribute, expected_attributes",
    [
        (255, "color_temp", {"brightness": 255, "color_temp": 370}),
        (255, "xy_color", {"brightness": 255, "xy_color": (0.323, 0.329)}),
        (120, "error", {"brightness": 120}),
    ],
)
@pytest.mark.asyncio
async def test_sync(
    sut, monkeypatch, mocker, max_brightness, color_attribute, expected_attributes
):
    sut.max_brightness = max_brightness
    sut.light = {"name": "test_light"}
    sut.transition = 300
    sut.add_transition = True
    sut.add_transition_turn_toggle = True
    sut.supported_features = LightSupport(
        FeatureSupport.encode({LightSupport.TRANSITION})
    )

    def fake_get_attribute(*args, **kwargs):
        if color_attribute == "error":
            raise ValueError()
        return color_attribute

    monkeypatch.setattr(sut, "get_attribute", fake_get_attribute)
    called_service_patch = mocker.patch.object(sut, "call_service")

    await sut.sync()

    called_service_patch.assert_called_once_with(
        "light/turn_on",
        entity_id="test_light",
        **{"transition": 0.3, **expected_attributes}
    )


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

    def fake_get_attribute(*args, **kwargs):
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
        (
            "color_temp",
            Stepper.TOGGLE,
            Stepper.TOGGLE_DOWN,
            "on",
            True,
            1,
            Stepper.TOGGLE_DOWN,
        ),
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

    def fake_get_attribute(*args, **kwargs):
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


@pytest.mark.parametrize(
    "value_attribute", [10, None],
)
@pytest.mark.asyncio
async def test_hold_loop(sut, mocker, value_attribute):
    attribute = "test_attribute"
    direction = Stepper.UP
    sut.value_attribute = value_attribute
    change_light_state_patch = mocker.patch.object(sut, "change_light_state")
    stepper = MinMaxStepper(1, 10, 10)
    sut.automatic_steppers = {attribute: stepper}

    # SUT
    exceeded = await sut.hold_loop(attribute, direction)

    if value_attribute is None:
        assert exceeded == True
    else:
        change_light_state_patch.assert_called_once_with(
            sut.value_attribute, attribute, direction, stepper, "hold"
        )
