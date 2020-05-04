"""
Bring full functionality to light and media player controllers.
From turning devices on/off to changing the color lights.

https://github.com/xaviml/controllerx
"""
from core import CallServiceController
from core import CustomLightController
from core import CustomMediaPlayerController
from core import CustomSwitchController
from core import CustomCoverController
from devices.aqara import *
from devices.ikea import *
from devices.lutron import *
from devices.philips import *
from devices.smartthings import *
from devices.trust import *
