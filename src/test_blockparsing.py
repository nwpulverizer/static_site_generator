import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType


class BlockParseTest(unittest.TestCase):
    def test_blockparse(self):
        test_multiline_md_str = "# This is a heading\n\nThis is a paragraph of text\nAnother line of the same p.\n\n*list item1\n*list item 2"
        expected = [
            "# This is a heading",
            "This is a paragraph of text\nAnother line of the same p.",
            "*list item1\n*list item 2",
        ]
        self.assertEqual(expected, markdown_to_blocks(test_multiline_md_str))

    def test_blockparse_oddnumber_of_blank_lines(self):
        test_string = "# Heading\n\n\n\n\nnow a paragraph.\n\n# Another heading"
        expected = ["# Heading", "now a paragraph.", "# Another heading"]
        self.assertEqual(expected, markdown_to_blocks(test_string))

    def test_blockparse_evennumber_of_blank_lines(self):
        test_string = "# Heading\n\n\n\n\nnow a paragraph.\n\n# Another heading"
        expected = ["# Heading", "now a paragraph.", "# Another heading"]
        self.assertEqual(expected, markdown_to_blocks(test_string))

    def text_blockparse_startswith_newline(self):
        test_string = "\n\n# Heading \n\nparagraph"
        expected = ["# Heading", "paragraph"]
        self.assertEqual(expected, markdown_to_blocks(test_string))

    def text_block_parse_endswith_newlines(self):
        test_string = "# Heading \n\nparagraph\n\n\n"
        expected = ["# Heading", "paragraph"]
        self.assertEqual(expected, markdown_to_blocks(test_string))

    def test_blockparse_with_empty_string(self):
        test_string = ""
        expected = []
        self.assertEqual(expected, markdown_to_blocks(test_string))

    def test_block_to_block_type_paragraph(self):
        block = "Here is a paragraph\nwith a newline!"
        expected = BlockType.paragraph
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_heading(self):
        block = "# Heading"
        expected = BlockType.heading
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_code(self):
        block = "``` a code block\n```"
        expected = BlockType.code
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_quote(self):
        block = "> Quote\n>line 2\n> line3"
        expected = BlockType.quote
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_notquote(self):
        block = ">Looks like a quite\nbut actually isn't"
        shouldnt_be = BlockType.quote
        self.assertNotEqual(shouldnt_be, block_to_block_type(block))

    def test_block_to_block_type_ulist(self):
        block = "* item 1\n* item 2"
        expected = BlockType.unordered_list
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_ulist_mixed(self):
        block = "* item 1\n- item 2"
        expected = BlockType.unordered_list
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_olist(self):
        block = "1. item 1\n2. item 2"
        expected = BlockType.ordered_list
        self.assertEqual(expected, block_to_block_type(block))

    def test_block_to_block_type_notolist(self):
        block = "1. item1\n5. item 2"
        shouldnt_be = BlockType.ordered_list
        self.assertNotEqual(shouldnt_be, block_to_block_type(block))

    def test_block_to_block_type_multi_digit_ol(self):
        block = "1. item\n2. item\n3. item\n4. item\n5. item\n6. item\n7. item\n8. item\n9. item\n10. item\n11. item"
        expected = BlockType.ordered_list
        self.assertEqual(expected, block_to_block_type(block))
