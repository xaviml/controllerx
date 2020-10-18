from cx_core.controller import TypeController
from cx_core.feature_support import FeatureSupport


class LightSupport(FeatureSupport):
    BRIGHTNESS = 1
    COLOR_TEMP = 2
    EFFECT = 4
    FLASH = 8
    COLOR = 16
    TRANSITION = 32
    WHITE_VALUE = 128

    def __init__(
        self, entity: str, controller: TypeController, update_supported_features: bool,
    ) -> None:
        super().__init__(
            entity,
            controller,
            [
                LightSupport.BRIGHTNESS,
                LightSupport.COLOR_TEMP,
                LightSupport.EFFECT,
                LightSupport.FLASH,
                LightSupport.COLOR,
                LightSupport.TRANSITION,
                LightSupport.WHITE_VALUE,
            ],
            update_supported_features,
        )
