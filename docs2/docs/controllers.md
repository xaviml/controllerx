{% set controllers = devices() %}

Currently **{{ controllers | length }}** devices are supported.

<table style="width:100%">
  <tr>
    <th>Model</th>
    <th>Integrations</th>
    <th>Picture</th>
  </tr>
  {% for device, controller_docs in controllers.items() %}
    <tr>
            <td style="vertical-align: middle;"><h3><a href="/controllers/{{ device }}">{{ device }}</a></h3></td>
            <td style="vertical-align: middle;">{{ controller_docs[0].integrations.values() | map(attribute="title") | join(", ") }}</td>
            <td style="vertical-align: middle;"><img src="/assets/images/{{ device }}.jpeg" /></td>
    </tr>
    {% endfor %}
</table>
