from typing import List

import pytest
from cx_core.feature_support import FeatureSupport
from cx_core.feature_support.light import LightSupport
from cx_core.type_controller import TypeController


@pytest.mark.parametrize(
    "number, expected_supported_features",
    [
        (1, [LightSupport.BRIGHTNESS]),
        (
            57,
            [
                LightSupport.BRIGHTNESS,
                LightSupport.FLASH,
                LightSupport.COLOR,
                LightSupport.TRANSITION,
            ],
        ),
        (
            149,
            [
                LightSupport.BRIGHTNESS,
                LightSupport.EFFECT,
                LightSupport.COLOR,
                LightSupport.WHITE_VALUE,
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_is_supported(
    fake_type_controller: TypeController,
    number: int,
    expected_supported_features: List[int],
):
    feature_support = FeatureSupport(fake_type_controller)
    feature_support._supported_features = number
    for expected_supported_feature in expected_supported_features:
        assert await feature_support.is_supported(expected_supported_feature)
