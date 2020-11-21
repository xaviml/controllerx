from cx_core.feature_support import FeatureSupport


class LightSupport(FeatureSupport):
    BRIGHTNESS = 1
    COLOR_TEMP = 2
    EFFECT = 4
    FLASH = 8
    COLOR = 16
    TRANSITION = 32
    WHITE_VALUE = 128

    features = [
        BRIGHTNESS,
        COLOR_TEMP,
        EFFECT,
        FLASH,
        COLOR,
        TRANSITION,
        WHITE_VALUE,
    ]
