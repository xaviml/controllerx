"""
Generate the supported controllers documentation into docs/controllers/:

- index.md: catalogue of all the supported devices
- <device>.md: one page per device
- devices.json: machine-readable catalogue (configuration builder, AI tools)

Zensical does not support the mkdocs-gen-files plugin, so this script must
be run before `zensical build` / `zensical serve`. The generated files are
git-ignored.
"""

import json
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

CURRENT_DIR = Path(__file__).parent
OUTPUT_DIR = CURRENT_DIR / "docs" / "controllers"

sys.path.insert(0, str(CURRENT_DIR))

from main import INTEGRATIONS, get_catalogue, get_devices  # noqa: E402


def main() -> None:
    env = Environment(
        loader=FileSystemLoader(searchpath=CURRENT_DIR),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    device_template = env.get_template("device_template.md")
    controllers_template = env.get_template("controllers_template.md")

    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    OUTPUT_DIR.mkdir(parents=True)

    devices = get_devices()
    for device in devices.values():
        content = device_template.render(device=device, INTEGRATIONS=INTEGRATIONS)
        (OUTPUT_DIR / f"{device.name}.md").write_text(content)

    integrations = [
        INTEGRATIONS[name].title
        for name in INTEGRATIONS
        if any(name in device.integrations_list for device in devices.values())
    ]
    types = [
        ct_type
        for _, ct_type in sorted(
            {
                (ct.order, ct.type)
                for device in devices.values()
                for ct in device.controller_type_docs
            }
        )
    ]
    (OUTPUT_DIR / "index.md").write_text(
        controllers_template.render(
            devices=devices,
            manufacturers=sorted(
                {d.manufacturer for d in devices.values()}, key=str.lower
            ),
            integrations=integrations,
            types=types,
        )
    )

    (OUTPUT_DIR / "devices.json").write_text(
        json.dumps(get_catalogue(devices), indent=2, ensure_ascii=False) + "\n"
    )

    print(f"Generated {len(devices)} device pages in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
