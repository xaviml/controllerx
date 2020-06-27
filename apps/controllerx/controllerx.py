"""
Bring full functionality to light and media player controllers.
From turning devices on/off to changing the color lights.

https://github.com/xaviml/controllerx
"""
from cx_core import CallServiceController
from cx_core import CustomLightController
from cx_core import CustomMediaPlayerController
from cx_core import CustomSwitchController
from cx_core import CustomCoverController
from cx_devices.aqara import *
from cx_devices.ikea import *
from cx_devices.lutron import *
from cx_devices.philips import *
from cx_devices.smartthings import *
from cx_devices.trust import *
