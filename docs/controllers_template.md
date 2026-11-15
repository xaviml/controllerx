---
title: Supported controllers
description: The {{ devices | length }} devices supported by ControllerX out of the box, with their manufacturer, controller types and integrations.
---

# Supported controllers

ControllerX supports **{{ devices | length }}** devices out of the box. Select your device to see its default button mapping and an example configuration, or use the [configuration builder](../start/config-builder.md) to generate the configuration for it.

If your device is not listed, you can still use it with a [custom mapping](../advanced/index.md) on top of the generic controllers (`LightController`, `MediaPlayerController`, `SwitchController`, `CoverController` and `Z2MLightController`).

!!! tip "For tools and AI assistants"

    This list is also available as [JSON](devices.json), including the controller classes and the default mapping of every device.

<div class="cx-filters" hidden>
  <input type="search" class="md-input cx-filter-search" placeholder="Search by model or manufacturer" aria-label="Search by model or manufacturer">
  <select class="cx-filter" data-column="Manufacturer" aria-label="Manufacturer">
    <option value="">All manufacturers</option>
{%- for manufacturer in manufacturers %}
    <option>{{ manufacturer }}</option>
{%- endfor %}
  </select>
  <select class="cx-filter" data-column="Integrations" aria-label="Integration">
    <option value="">All integrations</option>
{%- for integration in integrations %}
    <option>{{ integration }}</option>
{%- endfor %}
  </select>
  <select class="cx-filter" data-column="Controller types" aria-label="Controller type">
    <option value="">All controller types</option>
{%- for type in types %}
    <option>{{ type }}</option>
{%- endfor %}
  </select>
  <span class="cx-filter-count" aria-live="polite"></span>
</div>

<div class="cx-catalogue" markdown>

| Picture | Device | Manufacturer | Controller types | Integrations |
| --- | --- | --- | --- | --- |
{%- for device in devices.values() %}
| ![{{ device.title }}](../assets/controllers/{{ device.name }}.jpeg){ loading=lazy width="64" } | [{{ device.name }}]({{ device.name }}.md) | {{ device.manufacturer }} | {{ device.types | join(", ") }} | {{ device.integrations_titles | join(", ") }} |
{%- endfor %}

</div>
