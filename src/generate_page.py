import os

from markdown_to_html_node import markdown_to_html_node
from htmlnode import HTMLNode

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    content = read_file(from_path)
    title = extract_title(content)
    html = markdown_to_html_node(content).to_html()

    template = read_file(template_path)
    template = template.replace(r"{{ Title }}", title)
    template = template.replace(r"{{ Content }}", html)

    write_file(dest_path, template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    pass

def read_file(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Unable to read file {path}: {e}")

def write_file(path, content):
    try:
        path_to_file = os.path.split(path)[0]        
        if not os.path.exists(path_to_file):
            os.makedirs(path_to_file)

        with open(path, "w") as file:
            file.write(content)       
            print(f'Successfully wrote to "{path}" ({len(content)} characters written).')
    except Exception as e:
        raise Exception(f'Error: Could not write to "{path}", failed with exception: {e}')
    
def extract_title(markdown):
    if markdown:
        parts = markdown.split(" ", 1)
        if len(parts) > 1 and parts[0] == "#":
            return parts[1].split("\n", 1)[0]
    raise Exception("h1 header missing in markdown document.")