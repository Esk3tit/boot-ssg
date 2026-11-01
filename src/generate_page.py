import os

from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    if not markdown.startswith("# "):
        raise Exception("No h1 header")
    return markdown.split("\n", 1)[0][2:].strip()


def generate_page(from_path, template_path, dest_path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as t:
        template = t.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    final_page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as d:
        d.write(final_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = os.path.splitext(dest_path)[0] + ".html"
            print(f" * {from_path} -> {dest_path}")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)