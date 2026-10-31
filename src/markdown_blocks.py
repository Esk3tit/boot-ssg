import re
from enum import Enum
from htmlnode import ParentNode, HTMLNode
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    return [line.strip() for line in lines if line.strip() != ""]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s+.+$", block):
        return BlockType.HEADING
    if re.match(r"^```.*\n[\s\(\S\)]*?```$", block):
        return BlockType.CODE
    lines = block.splitlines()
    if all(re.match(r"^> ?.*", line) for line in lines):
        return BlockType.QUOTE
    if all(re.match(r"^- .*", line) for line in lines):
        return BlockType.UNORDERED_LIST
    for index, line in enumerate(lines, 1):
        match = re.match(r"^(\d+)\. .*", line)
        if not match or int(match.group(1)) != index:
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_html: list[HTMLNode] = []
    for block in blocks:
        lines = block.splitlines()
        match block_to_block_type(block):
            case BlockType.HEADING:
                match = re.match(r"^(#{1,6})\s+(.+)$", block)
                header_level = len(match.group(1))
                block_html.append(ParentNode(f"h{header_level}", text_to_children(match.group(2))))
            case BlockType.CODE:
                match = re.match(r"^```.*\n([\s\S]*?)```$", block)
                block_html.append(ParentNode("pre", [text_node_to_html_node(TextNode(match.group(1), TextType.CODE))]))
            case BlockType.QUOTE:
                inner = "\n".join(re.match(r"^ {0,3}> ?(.*)", line).group(1) for line in lines)
                block_html.append(ParentNode("blockquote", text_to_children(inner)))
            case BlockType.UNORDERED_LIST:
                lis = [ParentNode("li", text_to_children(re.match(r"^- (.*)", line).group(1))) for line in lines]
                block_html.append(ParentNode("ul", lis))            
            case BlockType.ORDERED_LIST:
                lis = [ParentNode("li", text_to_children(re.match(r"^(\d+)\. (.*)", line).group(2))) for line in lines]
                block_html.append(ParentNode("ol", lis))
            case BlockType.PARAGRAPH:
                block_html.append(ParentNode("p", text_to_children(" ".join(lines))))
    return ParentNode("div", block_html)