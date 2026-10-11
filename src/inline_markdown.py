import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # If there are matching pairs of delimiters the length of the split will always be odd, since
        # splitting on even amount of delimiters (matching means 2, even amount) you'll get odd len splits
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise Exception("Invalid Markdown Syntax")
        for i in range(len(splits)):
            if splits[i] == "":
                continue
            new_nodes.append(TextNode(splits[i], TextType.TEXT if i % 2 == 0 else text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Extract all images, and then split per tuple and loop thru all images and split once per tuple
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        curr_text = node.text
        for image_alt, image_link in images:
            sections = curr_text.split(f"![{image_alt}]({image_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            curr_text = sections[1]
        if curr_text != "":
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Extract all links, and then split per tuple and loop thru all links and split once per tuple
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        curr_text = node.text
        for link_alt, link_link in links:
            sections = curr_text.split(f"[{link_alt}]({link_link})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
            curr_text = sections[1]
        if curr_text != "":
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes

