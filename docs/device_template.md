<table>
    <tr>
      <th>Picture</th>
      <th>
        <a href="#">Controller types</a>
      </th>
      <th>Integrations</th>
    </tr>
    <tr>
      <td style="vertical-align: middle;"><img src="/controllerx/assets/controllers/{{ device }}.jpeg" /></td>
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
          {% for integration in controllers[0].integrations_list %}
          <li>
            {{ INTEGRATIONS_TITLES[integration] }} ({{ integration }})
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

{% for integration in controller.integrations_examples %}

=== "{{ integration["title"] }}"

    ```yaml
    example_app:
      module: controllerx
      class: {{ controller.cls }}{% if "attrs" not in integration %}
      integration: {{ integration["name"] }}{% else %}
      integration:
        name: {{ integration["name"] }}
      {% for attr_key, attr_value in integration["attrs"].items() %}  {{ attr_key }}: {{ attr_value }}{% endfor %}{% endif %}
      controller: {{ integration["controller"] }}
      {{ controller.domain }}: {{ controller.domain }}.my_entity_id
    ```

{% endfor %}
{% endfor %}
