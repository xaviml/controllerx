from typing import List

import pytest
from cx_core.feature_support import FeatureSupport
from cx_core.feature_support.light import LightSupport
from cx_core.type_controller import Entity, TypeController


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        (
            40,
            [
                LightSupport.FLASH,
                LightSupport.TRANSITION,
            ],
        ),
        (
            4,
            [
                LightSupport.EFFECT,
            ],
        ),
        (
            36,
            [
                LightSupport.EFFECT,
                LightSupport.TRANSITION,
            ],
        ),
    ],
)
async def test_is_supported(
    fake_type_controller: TypeController[Entity],
    number: int,
    expected_supported_features: List[int],
) -> None:
    feature_support = FeatureSupport(fake_type_controller)
    feature_support._supported_features = number
    for expected_supported_feature in expected_supported_features:
        assert await feature_support.is_supported(expected_supported_feature)
