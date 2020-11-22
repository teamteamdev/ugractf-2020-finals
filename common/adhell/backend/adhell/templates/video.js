{% extends "base.js" %}
{% block adhell %}<video id='{{ html_id }}' loop style='width: 100%;' autoplay src='{{ banner.content|safe }}'></video>{% endblock %}
{% block onload %}
const vd = document.querySelector('#{{ html_id }}');
vd.controls = false;
const lst = function() {
    vd.play();
    document.body.removeEventListener('click', lst);
}
document.body.addEventListener('click', lst);
{% endblock %}
