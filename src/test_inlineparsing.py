import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    string_to_TextNode,
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

    def test_split_nodes_links_single_link(self):
        text = TextNode("Here is text with a [link](https://image.com).", TextType.text)
        result = split_nodes_links([text])
        expected_result = [
            TextNode("Here is text with a ", TextType.text),
            TextNode("link", TextType.link, "https://image.com"),
            TextNode(".", TextType.text),
        ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_links_two_item_list(self):
        text = TextNode(
            "Here is text with a [link](https://image.com). Why not another one? [link2](https://image2.url)",
            TextType.text,
        )
        text2 = TextNode(
            "Here is text with a link again! [link3](https://image3.com). Why not another one? [link4](https://image4.url)",
            TextType.text,
        )
        result = split_nodes_links([text, text2])
        expected_result = [
            TextNode("Here is text with a ", TextType.text),
            TextNode("link", TextType.link, "https://image.com"),
            TextNode(". Why not another one? ", TextType.text),
            TextNode("link2", TextType.link, URL="https://image2.url"),
            TextNode("Here is text with a link again! ", TextType.text),
            TextNode("link3", TextType.link, "https://image3.com"),
            TextNode(". Why not another one? ", TextType.text),
            TextNode("link4", TextType.link, URL="https://image4.url"),
        ]
        self.assertEqual(result, expected_result)

    def test_string_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected_result = [
            TextNode("This is ", TextType.text),
            TextNode("text", TextType.bold),
            TextNode(" with an ", TextType.text),
            TextNode("italic", TextType.italic),
            TextNode(" word and a ", TextType.text),
            TextNode("code block", TextType.code),
            TextNode(" and an ", TextType.text),
            TextNode(
                "image",
                TextType.image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", TextType.text),
            TextNode("link", TextType.link, "https://boot.dev"),
        ]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_onlytext(self):
        text = "This is just text."
        expected_result = [TextNode("This is just text.", TextType.text)]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_onlyimage(self):
        text = "![alt](image.jpg)"
        expected_result = [TextNode("alt", TextType.image, "image.jpg")]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_onlylink(self):
        text = "[link](funlink.com)"
        expected_result = [TextNode("link", TextType.link, "funlink.com")]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_onlycode(self):
        text = "`h = 2`"
        expected_result = [TextNode("h = 2", TextType.code)]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_onlybold(self):
        text = "**bold**"
        expected_result = [TextNode("bold", TextType.bold)]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_onlyitalic(self):
        text = "*italic*"
        expected_result = [TextNode("italic", TextType.italic)]
        self.assertEqual(expected_result, string_to_TextNode(text))

    def test_string_to_text_nodes_bold_italic(self):
        text = "*italic text* and **bold**"
        expected_result = [
            TextNode("italic text", TextType.italic),
            TextNode(" and ", TextType.text),
            TextNode("bold", TextType.bold),
        ]
        self.assertEqual(expected_result, string_to_TextNode(text))


if __name__ == "__main__":
    unittest.main()
