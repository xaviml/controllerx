---
layout: page
title: Supported controllers
---

<table style="width:100%">
  <tr>
    <th>Model</th>
    <th>Controller type</th>
    <th>Class</th>
    <th>Delay</th>
    <th>Picture</th>
  </tr>
  {% for controller in site.data.controllers %}
    <tr>
            <td><a href="{{controller.link}}">{{ controller.name }}</a></td>
            <td>{{ controller.type }}</td>
            <td>{{ controller.class }}</td>
            <td>{{ controller.delay }}</td>
            <td><img src="{{controller.img}}"></td>
    </tr>
    {% endfor %}
</table>
