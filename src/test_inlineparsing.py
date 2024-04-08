import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
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

    def test_split_nodes_images_single_image(self):
        text = TextNode(
            "Here is text with an image ![image](https://image.com).", TextType.text
        )
        result = split_nodes_images([text])
        expected_result = [
            TextNode("Here is text with an image ", TextType.text),
            TextNode("image", TextType.image, "https://image.com"),
            TextNode(".", TextType.text),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_images_multiple_images(self):
        text = TextNode(
            "Here is text with an image ![image](https://image.com). Why not another one? ![image2](https://image2.url)",
            TextType.text,
        )
        result = split_nodes_images([text])
        expected_result = [
            TextNode("Here is text with an image ", TextType.text),
            TextNode("image", TextType.image, "https://image.com"),
            TextNode(". Why not another one? ", TextType.text),
            TextNode("image2", TextType.image, URL="https://image2.url"),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_images_justimage(self):
        text = TextNode("![image](onlyimage.com)", TextType.text)
        result = split_nodes_images([text])
        expected_result = [TextNode("image", TextType.image, "onlyimage.com")]
        self.assertEqual(result, expected_result)

    def test_split_nodes_images_2itemlist(self):
        text = TextNode(
            "Here is text with an image ![image](https://image.com). Why not another one? ![image2](https://image2.url)",
            TextType.text,
        )
        text2 = TextNode(
            "Here is text with an image again ![image3](https://image3.com). Why not another one? ![image4](https://image4.url)",
            TextType.text,
        )
        result = split_nodes_images([text, text2])
        expected_result = [
            TextNode("Here is text with an image ", TextType.text),
            TextNode("image", TextType.image, "https://image.com"),
            TextNode(". Why not another one? ", TextType.text),
            TextNode("image2", TextType.image, URL="https://image2.url"),
            TextNode("Here is text with an image again ", TextType.text),
            TextNode("image3", TextType.image, "https://image3.com"),
            TextNode(". Why not another one? ", TextType.text),
            TextNode("image4", TextType.image, URL="https://image4.url"),
        ]
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
