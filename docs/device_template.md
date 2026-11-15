---
title: {{ device.title }}
description: {{ device.description }}
---

# {{ device.title }}

![{{ device.title }}](../assets/controllers/{{ device.name }}.jpeg){ .cx-device-image width="180" }

- **Manufacturer:** {{ device.manufacturer }}
- **Device ID:** `{{ device.name }}`
- **Controller types:** {% for ct in device.controller_type_docs %}[{{ ct.type }}](#{{ ct.section }}) (`{{ ct.cls }}`){% if not loop.last %}, {% endif %}{% endfor %}
- **Integrations:** {% for name in device.integrations_list %}[{{ INTEGRATIONS[name].title }}](../{{ INTEGRATIONS[name].page }}) (`{{ name }}`){% if not loop.last %}, {% endif %}{% endfor %}

[Build the configuration for this device](../start/config-builder.md?device={{ device.name }}){ .md-button .md-button--primary }
{%- if device.notes %}

## Notes

{{ device.notes | trim }}
{%- endif %}
{%- for ct in device.controller_type_docs %}

## {{ ct.type }}

- **Class:** `{{ ct.cls }}`
- **Entity parameter:** `{{ ct.entity_arg }}`
{%- if ct.delay is not none %}
- **Default delay:** `{{ ct.delay }}ms`
{%- endif %}

### Default mapping { #{{ ct.section }}-default-mapping }

Each row shows the events fired by the device for each integration and the [predefined action](../advanced/predefined-actions.md#{{ ct.section }}) they trigger by default. You can change it with a [custom mapping](../advanced/index.md).

{{ ct.make_table("../advanced/predefined-actions.md") }}

### Example configuration { #{{ ct.section }}-example-configuration }
{% for example in ct.integrations_examples %}
=== "{{ example.title }}"

    ```yaml
{{ ct.example_yaml(example) | indent(4, first=true) }}
    ```
{% endfor %}
{%- endfor %}
