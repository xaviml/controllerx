import pytest

from cx_core.controller import TypeController
from tests.test_utils import hass_mock


class FakeTypeController(TypeController):
    def get_domain(self):
        return "domain"


@pytest.fixture
def sut(hass_mock):
    c = FakeTypeController()
    c.args = {}
    return c


# All entities from '{entity}' must be from {domain} domain (e.g. {domain}.bedroom)
# '{entity}' must be from {domain} domain (e.g. {domain}.bedroom)


@pytest.mark.parametrize(
    "entity, domain, entities, error_expected",
    [
        ("light.kitchen", "light", [], False),
        ("light1.kitchen", "light", [], True,),
        ("media_player.kitchen", "light", [], True,),
        ("media_player.bedroom", "media_player", [], False),
        ("group.all_lights", "light", ["light.light1", "light.light2"], False),
        ("group.all_lights", "light", ["light1.light1", "light2.light2"], True),
        ("group.all", "media_player", ["media_player.test", "light.test"], True),
    ],
)
@pytest.mark.asyncio
async def test_check_domain(
    sut, mocker, monkeypatch, entity, domain, entities, error_expected
):
    expected_error_message = ""
    if error_expected:
        if entities == []:
            expected_error_message = (
                f"'{entity}' must be from {domain} domain (e.g. {domain}.bedroom)"
            )
        else:
            expected_error_message = f"All entities from '{entity}' must be from {domain} domain (e.g. {domain}.bedroom)"

    async def fake_get_state(*args, **kwargs):
        return entities

    monkeypatch.setattr(sut, "get_state", fake_get_state)
    monkeypatch.setattr(sut, "get_domain", lambda *args: domain)

    if error_expected:
        with pytest.raises(ValueError) as e:
            await sut.check_domain(entity)
        assert str(e.value) == expected_error_message
    else:
        await sut.check_domain(entity)


@pytest.mark.parametrize(
    "entity_input, expected_calls", [("light.kitchen", 1), ("group.lights", 2),],
)
@pytest.mark.asyncio
async def test_get_entity_state(sut, mocker, monkeypatch, entity_input, expected_calls):
    stub_get_state = mocker.stub()

    async def fake_get_state(entity, attribute=None):
        stub_get_state(entity, attribute=attribute)
        return ["entity.test"]

    monkeypatch.setattr(sut, "get_state", fake_get_state)

    # SUT
    await sut.get_entity_state(entity_input, "attribute_test")

    # Checks
    if expected_calls == 1:
        stub_get_state.assert_called_once_with(entity_input, attribute="attribute_test")
    elif expected_calls == 2:
        stub_get_state.call_count == 2
        stub_get_state.assert_any_call(entity_input, attribute="entity_id")
        stub_get_state.assert_any_call("entity.test", attribute="attribute_test")
