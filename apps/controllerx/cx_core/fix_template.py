"""
This is a temporary module to fix AppDaemon 4.4.0 and 4.4.1 bug:

https://github.com/AppDaemon/appdaemon/issues/1747

It seems that the problem has been fixed (https://github.com/AppDaemon/appdaemon/pull/1750),
but it is not known when the fix will be released.

This module has a spcific function (similar to AppDaemon call) for template rendering.

This entire file can be deleted once the fix is in place officially from AppDaemon.
"""
import asyncio
import json
import traceback
from typing import TYPE_CHECKING, Any, Optional

import aiohttp

if TYPE_CHECKING:
    from cx_core.controller import Controller


def convert_json(data: Any, **kwargs: Any) -> str:
    return json.dumps(data, default=str, **kwargs)


domain = "template"
service = "render"


async def render_template(
    session: aiohttp.ClientSession, ha_url: str, data: Any, controller: "Controller"
) -> Optional[str]:
    if isinstance(data, str):
        data = {"entity_id": data}

    api_url = f"{ha_url}/api/template"

    try:
        async with session.post(api_url, json=data) as resp:
            if resp.status == 200 or resp.status == 201:
                result = await resp.text()
            else:
                controller.log(
                    f"Error calling Home Assistant service {domain}/{service}",
                    level="WARNING",
                )
                txt = await resp.text()
                controller.log(f"Code: {resp.status}, error: {txt}", level="WARNING")
                result = None

            return result
    except (asyncio.TimeoutError, asyncio.CancelledError):
        controller.log(
            f"Timeout in call_service({domain}/{service}, {data})", level="WARNING"
        )
    except aiohttp.client_exceptions.ServerDisconnectedError:
        controller.log(
            "HASS Disconnected unexpectedly during call_service()", level="WARNING"
        )
    except Exception:
        controller.log("-" * 60, level="ERROR")
        controller.log("Unexpected error during call_plugin_service()", level="ERROR")
        controller.log(f"Service: {domain}.{service} Arguments: {data}", level="ERROR")
        controller.log("-" * 60, level="ERROR")
        controller.log(traceback.format_exc(), level="ERROR")
        controller.log("-" * 60, level="ERROR")
    return None
