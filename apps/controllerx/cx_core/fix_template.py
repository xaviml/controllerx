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
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiohttp

if TYPE_CHECKING:
    from cx_core.controller import Controller


def convert_json(data: Any, **kwargs: Any) -> str:
    return json.dumps(data, default=str, **kwargs)


domain = "template"
service = "render"


async def render_template(
    config: Dict[str, Any], data: Any, controller: "Controller"
) -> Optional[str]:
    if isinstance(data, str):
        data = {"entity_id": data}

    if "token" in config:
        headers = {"Authorization": "Bearer {}".format(config["token"])}
    elif "ha_key" in config:
        headers = {"x-ha-access": config["ha_key"]}
    else:
        headers = {}

    api_url = "{}/api/template".format(config["ha_url"])

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(), json_serialize=convert_json
        ) as session:
            async with session.post(
                api_url, headers=headers, json=data, verify_ssl=config["cert_verify"]
            ) as resp:
                if resp.status == 200 or resp.status == 201:
                    result = await resp.text()
                else:
                    controller.log.warning(
                        "Error calling Home Assistant service %s/%s",
                        domain,
                        service,
                    )
                    txt = await resp.text()
                    controller.log.warning("Code: %s, error: %s", resp.status, txt)
                    result = None

                return result
    except (asyncio.TimeoutError, asyncio.CancelledError):
        controller.log(
            "Timeout in call_service(%s/%s, %s)", domain, service, data, level="WARNING"
        )
    except aiohttp.client_exceptions.ServerDisconnectedError:
        controller.log(
            "HASS Disconnected unexpectedly during call_service()", level="WARNING"
        )
    except Exception:
        controller.log("-" * 60, level="ERROR")
        controller.log("Unexpected error during call_plugin_service()", level="ERROR")
        controller.log(
            "Service: %s.%s Arguments: %s", domain, service, data, level="ERROR"
        )
        controller.log("-" * 60, level="ERROR")
        controller.log(traceback.format_exc(), level="ERROR")
        controller.log("-" * 60, level="ERROR")
    return None
