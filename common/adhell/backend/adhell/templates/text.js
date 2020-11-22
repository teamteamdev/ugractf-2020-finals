{% extends "base.js" %}
{% block adhell %}<link href='https://fonts.googleapis.com/css2?family=Lobster&display=swap' rel='stylesheet'/><p id='{{ html_id }}' style='font-family: lobster, cursive; line-height: 1em; font-size: 1.5em; padding: 0.5em; margin: 0;'>{{ banner.content|safe }}</p>{% endblock %}
