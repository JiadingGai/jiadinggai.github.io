---
layout: page
title: projects
permalink: /projects/
description: Selected research and engineering projects.
---

{% assign sorted_projects = site.projects | sort: "importance" %}

<ul class="list-plain">
  {% for project in sorted_projects %}
    <li class="item">
      <h2>{{ project.title }}</h2>
      {% if project.description %}
        <p class="item-meta">{{ project.description }}</p>
      {% endif %}
      {{ project.content | markdownify }}
    </li>
  {% endfor %}
</ul>
