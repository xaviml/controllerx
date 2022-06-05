import os
import sys

import mkdocs_gen_files
from jinja2 import Environment, FileSystemLoader, select_autoescape

currentdir = os.path.dirname(__file__)
sys.path.insert(0, currentdir)

from main import INTEGRATIONS_TITLES, get_devices  # noqa

devices = get_devices()

env = Environment(
    loader=FileSystemLoader(searchpath="./"), autoescape=select_autoescape()
)

template = env.get_template("device_template.md")

for device, controller_docs in devices.items():
    with mkdocs_gen_files.open(f"controllers/{device}.md", "w") as f:
        print(
            template.render(
                controller_docs=controller_docs,
                INTEGRATIONS_TITLES=INTEGRATIONS_TITLES,
            ),
            file=f,
        )
