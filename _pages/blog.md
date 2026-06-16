---
layout: default
permalink: /blog/
title: blog
nav: true
nav_order: 5
pagination:
  enabled: false
---

<div class="post">

{% assign blog_name_size = site.blog_name | size %}
{% assign blog_description_size = site.blog_description | size %}

{% if blog_name_size > 0 or blog_description_size > 0 %}
  <div class="header-bar">
    <h1>{{ site.blog_name }}</h1>
    <h2>{{ site.blog_description }}</h2>
  </div>
{% endif %}

{% if site.display_tags and site.display_tags.size > 0 or site.display_categories and site.display_categories.size > 0 %}
  <div class="tag-category-list">
    <ul class="p-0 m-0">
      {% for tag in site.display_tags %}
        <li>
          <i class="fa-solid fa-hashtag fa-sm"></i> <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}">{{ tag }}</a>
        </li>
        {% unless forloop.last %}
          <p>&bull;</p>
        {% endunless %}
      {% endfor %}
      {% if site.display_categories.size > 0 and site.display_tags.size > 0 %}
        <p>&bull;</p>
      {% endif %}
      {% for category in site.display_categories %}
        <li>
          <i class="fa-solid fa-tag fa-sm"></i> <a href="{{ category | slugify | prepend: '/blog/category/' | relative_url }}">{{ category }}</a>
        </li>
        {% unless forloop.last %}
          <p>&bull;</p>
        {% endunless %}
      {% endfor %}
    </ul>
  </div>
{% endif %}

<ul class="post-list">
{% for post in site.posts %}
  {% assign read_time = post.content | number_of_words | divided_by: 180 | plus: 1 %}
  {% assign year = post.date | date: "%Y" %}
  <li>
    <h3>
      <a class="post-title" href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h3>
    <p>{{ post.description }}</p>
    <p class="post-meta">
      {{ read_time }} min read &nbsp; &middot; &nbsp;
      {{ post.date | date: '%B %d, %Y' }}
    </p>
    <p class="post-tags">
      <a href="{{ year | prepend: '/blog/' | relative_url }}">
        <i class="fa-solid fa-calendar fa-sm"></i> {{ year }}
      </a>
      {% for tag in post.tags %}
        &nbsp; &middot; &nbsp;
        <a href="{{ tag | slugify | prepend: '/blog/tag/' | relative_url }}">
          <i class="fa-solid fa-hashtag fa-sm"></i> {{ tag }}
        </a>
      {% endfor %}
      {% for category in post.categories %}
        &nbsp; &middot; &nbsp;
        <a href="{{ category | slugify | prepend: '/blog/category/' | relative_url }}">
          <i class="fa-solid fa-tag fa-sm"></i> {{ category }}
        </a>
      {% endfor %}
    </p>
  </li>
{% endfor %}
</ul>

</div>
