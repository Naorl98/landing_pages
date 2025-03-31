import os
import shutil
import datetime
from jinja2 import Environment, FileSystemLoader

def get_templates():
    templates_path = os.path.join(os.getcwd(), "templates")
    return [name for name in os.listdir(templates_path) if os.path.isdir(os.path.join(templates_path, name))]

def get_themes():
    return ["dark", "light", "vibrant"]

def generate_landing_page(template_name, data):
    env = Environment(loader=FileSystemLoader(f"templates/{template_name}"))
    template = env.get_template("index.html")

    output_html = template.render(
        title=data.get("title"),
        description=data.get("description"),
        email=data.get("email"),
        phone=data.get("phone"),
        links=data.get("links", []),  # each link is a dict: { "url": ..., "title": ... }
        theme=data.get("theme"),
        background_image=data.get("background_image"),
        logo_image=data.get("logo_image"),
        logo_position=data.get("logo_position")
    )

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", f"landing_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    # Copy static files (optional)
    static_src = os.path.join("templates", template_name, "assets")
    static_dst = os.path.join(output_dir, "assets")
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst)

    return index_path
