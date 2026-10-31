import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading1(self):
        md = "# Heading 1"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_heading2(self):
        md = "## Heading 2"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_heading3(self):
        md = "### Heading 3"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_heading4(self):
        md = "#### Heading 4"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_heading5(self):
        md = "##### Heading 5"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_heading6(self):
        md = "###### Heading 6"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.HEADING
        )

    def test_heading_invalid(self):
        md = "####### Heading 7"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type, BlockType.PARAGRAPH
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestBlockToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading with **bold**

###### Smallest heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with <b>bold</b></h1><h6>Smallest heading</h6></div>",
        )

    def test_quote(self):
        md = """
> This is a _quote_
> that spans lines
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <i>quote</i>\nthat spans lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First **item**
- Second item
- Third with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First <b>item</b></li><li>Second item</li><li>Third with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First _item_
2. Second item
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First <i>item</i></li><li>Second item</li><li>Third item</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """
## Title

Intro paragraph
on two lines

> A quote

- a
- b

1. one
2. two
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>Title</h2><p>Intro paragraph on two lines</p><blockquote>A quote</blockquote><ul><li>a</li><li>b</li></ul><ol><li>one</li><li>two</li></ol></div>",
        )



if __name__ == "__main__":
    unittest.main()
