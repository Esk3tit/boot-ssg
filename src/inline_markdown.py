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