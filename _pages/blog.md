---
layout: page
permalink: /blog/
title: blog
description: Technical notes and research updates.
---

<ul class="post-list">
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <p class="item-meta">{{ post.date | date: "%B %-d, %Y" }}</p>
      {% if post.description %}
        <p>{{ post.description }}</p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
