def markdown_to_blocks(markdown: str) -> list[str]:
    lines = markdown.split("\n\n")
    return [line.strip() for line in lines if line.strip() != ""]