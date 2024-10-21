import os
import shutil

from markdown_to_blocks import *

def copy_dir():
    target = "./public"

    # clear contents of public
    if os.path.exists(target):
        shutil.rmtree(target)
        print("target already exists clearing it out")

    #os.mkdir(target)
    shutil.copytree("./static", target)
    # copy contents of src into public
    pass

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")

    if os.path.isfile(from_path):
        with open(from_path) as file:
            markdown = file.read()
            title = extract_title(markdown)
            node = markdown_to_html_node(markdown)
        if os.path.isfile(template_path):
            with open(template_path) as template_file:
                template = template_file.read()
                template = template.replace("{{ Title }}", title)
                template = template.replace("{{ Content }}", node.to_html())
        if os.path.isfile(dest_path):
            os.remove(dest_path)
        with open(dest_path, "w") as index_html:
            index_html.write(template)
