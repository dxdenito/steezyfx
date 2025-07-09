import os

def create_tool_template(slug):
    folder_path = os.path.join("templates","tools")
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, f"{slug}.html")
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            f.write("""\
{% extends 'layout.html' %}
{% block section %}  

{% endblock %}   
            """)