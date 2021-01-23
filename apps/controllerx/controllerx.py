"""
Create controller-based automations with ease to control your home devices and scenes.

https://github.com/xaviml/controllerx
"""
from cx_core import (
    CallServiceController,
    Controller,
    CoverController,
    CustomCoverController,
    CustomLightController,
    CustomMediaPlayerController,
    CustomSwitchController,
    LightController,
    MediaPlayerController,
    SwitchController,
)
from cx_devices.aqara import *
from cx_devices.ikea import *
from cx_devices.legrand import *
from cx_devices.livarno import *
from cx_devices.lutron import *
from cx_devices.muller_licht import *
from cx_devices.osram import *
from cx_devices.phillips import *
from cx_devices.rgb_genie import *
from cx_devices.smartthings import *
from cx_devices.sonoff import *
from cx_devices.terncy import *
from cx_devices.trust import *
