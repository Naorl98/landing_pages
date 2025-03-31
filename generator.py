import os
import json
import shutil
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

TEMPLATE_DIR = "templates"
THEME_DIR = "themes"
OUTPUT_DIR = "output"

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def get_templates():
    return [
        f"{folder}/index.html"
        for folder in os.listdir(TEMPLATE_DIR)
        if os.path.isdir(os.path.join(TEMPLATE_DIR, folder))
           and os.path.isfile(os.path.join(TEMPLATE_DIR, folder, "index.html"))
    ]


def get_themes():
    return [
        f.replace(".json", "")
        for f in os.listdir(THEME_DIR)
        if f.endswith(".json")
    ]


def load_theme(theme_name):
    theme_path = os.path.join(THEME_DIR, f"{theme_name}.json")
    with open(theme_path, "r") as f:
        return json.load(f)


def generate_landing_page(template_path, data):
    # Extract folder and file name
    folder_name, file_name = template_path.split("/")
    template = env.get_template(f"{folder_name}/{file_name}")
    theme = load_theme(data.get("theme", "blue"))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_title = "".join(c for c in data["title"] if c.isalnum() or c in ("_", "-")).rstrip()
    output_name = f"{safe_title}_{timestamp}"
    output_dir = os.path.join(OUTPUT_DIR, output_name)

    os.makedirs(output_dir, exist_ok=True)

    # Handle image files
    background_image = data.get("background_image")
    logo_image = data.get("logo_image")

    def copy_image(source_path, name):
        if source_path and os.path.exists(source_path):
            ext = os.path.splitext(source_path)[1]
            dest_path = os.path.join(output_dir, f"{name}{ext}")
            shutil.copy(source_path, dest_path)
            return f"{name}{ext}"
        return ""

    bg_filename = copy_image(background_image, "background")
    logo_filename = copy_image(logo_image, "logo")

    # Render HTML
    rendered = template.render(
        title=data.get("title", ""),
        description=data.get("description", ""),
        email=data.get("email", ""),
        phone=data.get("phone", ""),
        links=data.get("links", []),
        theme=theme,
        background_image=bg_filename,
        logo_image=logo_filename,
        logo_position=data.get("logo_position", "none")
    )

    # Save HTML file
    html_output_path = os.path.join(output_dir, "index.html")
    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    return html_output_path
