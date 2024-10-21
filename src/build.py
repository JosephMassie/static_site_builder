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

def generate_pages_recursive(dir_path: str, template_path: str, dest_dir_path: str):
    paths = os.listdir(dir_path)
    
    for path in paths:
        full_path = os.path.join(dir_path, path)
        print(f"checking {full_path}")

        if os.path.isfile(full_path):
            new_path = path.rstrip(".md") + ".html"
            dest_path = os.path.join(dest_dir_path, new_path)
            print(f"- is a file generating page @ {dest_path}")
            generate_page(full_path, template_path, dest_path)
        elif os.path.isdir(full_path):
            print(f"- is a directory creating a new directory in {dest_dir_path}")
            new_dir = os.path.join(dest_dir_path, path)
            os.mkdir(new_dir)
            generate_pages_recursive(full_path, template_path, new_dir)
        else:
            raise Exception(f"invalid entry found @ '{full_path}'")
