import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world   "), "Hello world")

    def test_title_followed_by_blocks(self):
        md = """# Tolkien Fan Club

This is a paragraph.

- item one
- item two
"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_title_followed_by_line_in_same_block(self):
        md = "# Title\nThis line is not part of the title"
        self.assertEqual(extract_title(md), "Title")

    def test_no_header_raises(self):
        with self.assertRaises(Exception):
            extract_title("Just a paragraph")

    def test_empty_markdown_raises(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_h1_not_first_raises(self):
        md = """Some intro text

# Title
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_h2_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Not an h1")

    def test_hash_without_space_raises(self):
        with self.assertRaises(Exception):
            extract_title("#NotAHeader")


if __name__ == "__main__":
    unittest.main()
