import unittest

from markdown_blocks import markdown_to_blocks,block_to_block_type,BlockType


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
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Small"), BlockType.HEADING)
 
    def test_bad_heading(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
 
    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
 
    def test_bad_code(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)
 
    def test_quote(self):
        self.assertEqual(block_to_block_type("> a\n>b\n> c"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> a\nb"), BlockType.PARAGRAPH)
 
    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- a\n- b\n- c"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- a\n-b"), BlockType.PARAGRAPH)
 
    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. a\n2. b\n3. c"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. a\n3. b"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("2. a\n3. b"), BlockType.PARAGRAPH)
 
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text\nover two lines"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
