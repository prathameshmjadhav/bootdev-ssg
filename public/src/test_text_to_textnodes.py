import unittest

from split_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType

# ^ replace "your_module" with whatever file these are actually defined in


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_plain_text_only(self):
        # No delimiter present -> node passes through unchanged
        old_nodes = [TextNode("Just plain text here.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Just plain text here.", TextType.TEXT),
            ],
        )

    def test_italic_in_middle(self):
        old_nodes = [TextNode("I don't want to eat _italian_ food.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("I don't want to eat ", TextType.TEXT),
                TextNode("italian", TextType.ITALIC),
                TextNode(" food.", TextType.TEXT),
            ],
        )

    def test_bold_at_start(self):
        old_nodes = [TextNode("**What** is this", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("What", TextType.BOLD),
                TextNode(" is this", TextType.TEXT),
            ],
        )

    def test_bold_at_end(self):
        old_nodes = [TextNode("is this **What**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("is this ", TextType.TEXT),
                TextNode("What", TextType.BOLD),
            ],
        )

    def test_multiple_bold_pairs(self):
        old_nodes = [TextNode("**a** and **b**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
        )

    def test_code_delimiter(self):
        old_nodes = [TextNode("Run `pytest` to test.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("pytest", TextType.CODE),
                TextNode(" to test.", TextType.TEXT),
            ],
        )

    def test_multiple_sentences_in_list(self):
        # Two separate TextNodes in old_nodes, only one has the delimiter
        old_nodes = [
            TextNode("I like _italian_ food.", TextType.TEXT),
            TextNode("She wore a red dress.", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("I like ", TextType.TEXT),
                TextNode("italian", TextType.ITALIC),
                TextNode(" food.", TextType.TEXT),
                TextNode("She wore a red dress.", TextType.TEXT),
            ],
        )

    def test_chained_calls_for_multiple_delimiters(self):
        # Simulates calling split_nodes_delimiter multiple times,
        # like text_to_textnodes would, across a list of sentences
        old_nodes = [
            TextNode("I like _italian_ food.", TextType.TEXT),
            TextNode("She wore a **red** dress.", TextType.TEXT),
        ]
        nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            nodes,
            [
                TextNode("I like ", TextType.TEXT),
                TextNode("italian", TextType.ITALIC),
                TextNode(" food.", TextType.TEXT),
                TextNode("She wore a ", TextType.TEXT),
                TextNode("red", TextType.BOLD),
                TextNode(" dress.", TextType.TEXT),
            ],
        )

    def test_non_text_node_is_skipped(self):
        # A node that's already BOLD should not be touched by an ITALIC pass
        old_nodes = [TextNode("already bold", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        old_nodes = [TextNode("This is _broken italic text.", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

    def test_empty_old_nodes_list(self):
        new_nodes = split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [])


if __name__ == "__main__":
    unittest.main()
