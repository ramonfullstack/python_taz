## [{{versiondata.version}}]() {{versiondata.date}}


{% for section, _ in sections.items() %}
{% if sections[section] %}
{% for category, val in definitions.items() if category in sections[section]%}
### {{ definitions[category]['name'] }}

{% if definitions[category]['showcontent'] %}
{% for text, _ in sections[section][category].items() %}
- {{ text }}
{% endfor %}

{% else %}
- {{ sections[section][category]['']|join(', ') }}

{% endif %}
{% if sections[section][category]|length == 0 %}
No significant changes.
{% endif %}
{% endfor %}
{% else %}
No significant changes.

{% endif %}
{% endfor %}