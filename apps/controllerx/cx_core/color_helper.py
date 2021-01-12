from typing import List, Tuple, Union

Colors = List[Tuple[float, float]]

# These are the 24 colors that appear in the circle color of home assistant
default_color_wheel = [
    (0.701, 0.299),
    (0.667, 0.284),
    (0.581, 0.245),
    (0.477, 0.196),
    (0.385, 0.155),
    (0.301, 0.116),
    (0.217, 0.077),
    (0.157, 0.05),
    (0.136, 0.04),
    (0.137, 0.065),
    (0.141, 0.137),
    (0.146, 0.238),
    (0.323, 0.329),  # 12; white color middle
    (0.151, 0.343),
    (0.157, 0.457),
    (0.164, 0.591),
    (0.17, 0.703),
    (0.172, 0.747),
    (0.199, 0.724),
    (0.269, 0.665),
    (0.36, 0.588),
    (0.444, 0.517),
    (0.527, 0.447),
    (0.612, 0.374),
    (0.677, 0.319),
]

# These are the xy colors translated from color temperature (2000K to 6488K)
# They were extracted from here https://www.waveformlighting.com/files/blackBodyLocus_1.txt
color_temp_wheel = [
    (0.527, 0.413),
    (0.507, 0.415),
    (0.489, 0.415),
    (0.472, 0.413),
    (0.456, 0.41),
    (0.442, 0.406),
    (0.428, 0.401),
    (0.416, 0.396),
    (0.406, 0.391),
    (0.396, 0.386),
    (0.386, 0.38),
    (0.378, 0.375),
    (0.37, 0.37),
    (0.363, 0.365),
    (0.357, 0.361),
    (0.351, 0.358),
    (0.345, 0.355),
    (0.34, 0.352),
    (0.336, 0.349),
    (0.331, 0.346),
    (0.327, 0.343),
    (0.323, 0.339),
    (0.32, 0.336),
    (0.317, 0.333),
    (0.314, 0.33),
]

COLOR_WHEELS = {
    "default_color_wheel": default_color_wheel,
    "color_temp_wheel": color_temp_wheel,
}


def get_color_wheel(colors: Union[str, Colors]) -> Colors:
    if isinstance(colors, str):
        if colors not in COLOR_WHEELS:
            raise ValueError(
                f"`{colors}` is not an option for `color_wheel`. Options are: {list(COLOR_WHEELS.keys())}"
            )
        return COLOR_WHEELS[colors]
    elif isinstance(colors, (list, tuple)):
        return colors
    else:
        raise ValueError(
            f"Type {type(colors)} is not supported for `color_wheel` attribute"
        )
