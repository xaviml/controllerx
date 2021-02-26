---
layout: page
title: Supported controllers
---

{% assign controllers = site.data.controllers | sort %}

Currently **{{ controllers.size }}** devices are supported.

<table style="width:100%">
  <tr>
    <th>Model</th>
    <th>Integrations</th>
    <th>Picture</th>
  </tr>
  {% for controller_obj in controllers %}
    {% assign key = controller_obj[0] %}
    {% assign controller = controller_obj[1] %}
    {% assign integration_names = controller.integrations | map: "codename" | join: ", " %}
    <tr>
            <td><a href="/controllerx/controllers/{{key}}">{{ controller.name }}</a></td>
            <td>{{ integration_names }}</td>
            <td><img src="/controllerx/assets/img/{{ key }}.jpeg" /></td>
    </tr>
    {% endfor %}
</table>
