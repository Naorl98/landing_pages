import os
import shutil
import base64
from datetime import datetime
from jinja2 import Environment, FileSystemLoader


def get_templates():
    return [name for name in os.listdir("templates") if os.path.isdir(os.path.join("templates", name))]


def get_themes():
    return ["default", "light", "dark"]


def encode_image_base64(image_path):
    if not os.path.isfile(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return "data:image/{};base64,".format(image_path.split(".")[-1]) + base64.b64encode(img_file.read()).decode("utf-8")


def generate_landing_page(template_name, data):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"output/{template_name}_{now}"
    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(f"templates/{template_name}"))
    template = env.get_template("index.html")

    # Convert images to base64
    data["background_image"] = encode_image_base64(data.get("background_image", ""))
    data["logo_image"] = encode_image_base64(data.get("logo_image", ""))

    for link in data.get("links", []):
        link["icon"] = encode_image_base64(link.get("icon", ""))

    for img in data.get("gallery_images", []):
        img["img"] = encode_image_base64(img.get("path", ""))

    rendered_html = template.render(**data)

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    return output_path
