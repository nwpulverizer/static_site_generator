import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class InlineParseTest(unittest.TestCase):
    def test_inline_split_code(self):
        node = TextNode("Text with a `code block` more words", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        should_return = [
            TextNode("Text with a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" more words", TextType.text),
        ]
        self.assertEqual(new_nodes, should_return)

    def test_inline_split_two_codeblocks(self):
        node = TextNode(
            "Text with a `code block` more words `another code block`", TextType.text
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        should_return = [
            TextNode("Text with a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" more words ", TextType.text),
            TextNode("another code block", TextType.code),
        ]
        self.assertEqual(new_nodes, should_return)

    def test_inline_split_starts_with_code(self):
        node = TextNode("`code block` and now words!", TextType.text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code)
        should_return = [
            # what should I do with blank stirngs?
            TextNode("code block", TextType.code),
            TextNode(" and now words!", TextType.text),
        ]
        self.assertEqual(new_nodes, should_return)

    def test_inline_split_bold(self):
        node = TextNode("Text with a **bold** word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        should_return = [
            TextNode("Text with a ", TextType.text),
            TextNode("bold", TextType.bold),
            TextNode(" word", TextType.text),
        ]
        self.assertEqual(new_nodes, should_return)

    def test_inline_split_italic(self):
        node = TextNode("Text with a *italic* word", TextType.text)
        new_nodes = split_nodes_delimiter([node], "*", TextType.italic)
        should_return = [
            TextNode("Text with a ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" word", TextType.text),
        ]
        self.assertEqual(new_nodes, should_return)

    def test_inline_split_input_bold(self):
        node = TextNode("bold node", TextType.bold)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold)
        should_return = [TextNode("bold node", TextType.bold)]
        self.assertEqual(new_nodes, should_return)

    def test_extract_image(self):
        text = "This is text with an ![image](url.image) and ![another](image2.url)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(
            extracted_images, [("image", "url.image"), ("another", "image2.url")]
        )

    def test_extract_link(self):
        text = "This is text with a [hyperlink](hyperlink.url)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links, [("hyperlink", "hyperlink.url")])

    def test_extract_nolinks(self):
        text = "This is text without links"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links, [])

    def test_extract_noimages(self):
        text = "This is text without images"
        extracted_links = extract_markdown_images(text)
        self.assertEqual(extracted_links, [])


if __name__ == "__main__":
    unittest.main()
