import pytest
from cx_core.feature_support import FeatureSupport
from cx_core.type_controller import Entity, TypeController


@pytest.mark.parametrize(
    "number, feature, expected_is_supported",
    [
        (15, 16, False),
        (16, 2, False),
        (31, 64, False),
        (70, 4, True),
        (9, 8, True),
        (0, 0, False),
    ],
)
async def test_is_supported(
    fake_type_controller: TypeController[Entity],
    number: int,
    feature: int,
    expected_is_supported: bool,
) -> None:
    feature_support = FeatureSupport(fake_type_controller)
    feature_support._supported_features = number
    is_supported = await feature_support.is_supported(feature)
    assert is_supported == expected_is_supported


@pytest.mark.parametrize(
    "number, feature, expected_is_supported",
    [
        (15, 16, True),
        (16, 2, True),
        (31, 64, True),
        (70, 4, False),
        (9, 8, False),
        (0, 0, True),
    ],
)
async def test_not_supported(
    fake_type_controller: TypeController[Entity],
    number: int,
    feature: int,
    expected_is_supported: bool,
) -> None:
    feature_support = FeatureSupport(fake_type_controller)
    feature_support._supported_features = number
    is_supported = await feature_support.not_supported(feature)
    assert is_supported == expected_is_supported
