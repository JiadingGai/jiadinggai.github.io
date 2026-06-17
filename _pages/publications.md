---
layout: page
permalink: /publications/
title: publications
description: Selected publications and technical reports.
---

<ul class="list-plain">
  {% for pub in site.data.publications %}
    <li class="item">
      <p class="item-title">{{ pub.title }}{% if pub.award %}<span class="badge">{{ pub.award }}</span>{% endif %}</p>
      <p class="item-meta">{{ pub.authors }}. {{ pub.venue }}, {{ pub.year }}.</p>
      {% if pub.note %}
        {{ pub.note | markdownify }}
      {% endif %}
      {% if pub.links %}
        <p class="item-links">
          {% for link in pub.links %}
            <a href="{{ link.url }}">{{ link.label }}</a>
          {% endfor %}
        </p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
