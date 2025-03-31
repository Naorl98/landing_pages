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
        links=data.get("links", []),
        theme=data.get("theme"),
        background_image=data.get("background_image"),
        logo_image=data.get("logo_image"),
        logo_position=data.get("logo_position"),
        gallery_images=[]
    )

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", f"landing_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    gallery_data = []
    if data.get("gallery_images"):
        gallery_dir = os.path.join(output_dir, "gallery")
        os.makedirs(gallery_dir, exist_ok=True)
        for i, item in enumerate(data["gallery_images"]):
            src = item.get("path")
            caption = item.get("caption", "")
            ext = os.path.splitext(src)[1]
            dest_filename = f"image_{i+1}{ext}"
            dest_path = os.path.join(gallery_dir, dest_filename)
            shutil.copy(src, dest_path)
            gallery_data.append({"img": f"gallery/{dest_filename}", "caption": caption})

        output_html = template.render(
            title=data.get("title"),
            description=data.get("description"),
            email=data.get("email"),
            phone=data.get("phone"),
            links=data.get("links", []),
            theme=data.get("theme"),
            background_image=data.get("background_image"),
            logo_image=data.get("logo_image"),
            logo_position=data.get("logo_position"),
            gallery_images=gallery_data
        )

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    return index_path