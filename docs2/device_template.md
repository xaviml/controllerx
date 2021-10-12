<table>
    <tr>
      <th>Picture</th>
      <th>
        <a href="#">Controller types</a>
      </th>
      <th>Integrations</th>
    </tr>
    <tr>
      <td style="vertical-align: middle;"><img src="/assets/images/{{ device }}.jpeg" /></td>
      <td style="vertical-align: middle;">
        <ul>
          {% for ctrl in controllers %}
          <li>
            <a href="#{{ ctrl.type | lower | replace(' ','-') }}">{{ ctrl.type }}</a> — <code>{{ctrl.cls}}</code>
          </li>
          {% endfor %}
        </ul>
      </td>
      <td style="vertical-align: middle;">
        <ul>
          {% for key, integration in controllers[0].integrations.items() %}
          <li>
            {{ integration["title"] }} ({{ key }})
          </li>
          {% endfor %}
        </ul>
      </td>
    </tr>
  </table>
{% for controller in controllers %}

## {{ controller.type }}

Class: `{{ controller.cls }}`

{% if controller.delay is not none%}
Default delay: `{{ controller.delay }}ms`
{% endif %}

Default mapping:

{{ controller.make_table() }}

{% for key, integration in controller.integrations.items() %}

=== "{{ integration["title"] }}"

    ```yaml
    example_app:
      module: controllerx
      class: {{ controller.cls }}
      integration: {{ key }}
      controller: {{ integration["controller"] }}
      {{ controller.domain }}: {{ controller.domain }}.my_entity_id
    ```

{% endfor %}
{% endfor %}
