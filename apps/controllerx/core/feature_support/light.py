from core.feature_support import FeatureSupport, SupportedFeatureNumber


class LightSupport(FeatureSupport):
    BRIGHTNESS = 1
    COLOR_TEMP = 2
    EFFECT = 4
    FLASH = 8
    COLOR = 16
    TRANSITION = 32
    WHITE_VALUE = 128

    def __init__(self, number: SupportedFeatureNumber) -> None:
        super().__init__(
            number,
            [
                LightSupport.BRIGHTNESS,
                LightSupport.COLOR_TEMP,
                LightSupport.EFFECT,
                LightSupport.FLASH,
                LightSupport.COLOR,
                LightSupport.TRANSITION,
                LightSupport.WHITE_VALUE,
            ],
        )
