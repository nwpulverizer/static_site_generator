import unittest
from textnode import TextNode, TextType
from text_to_html import text_node_to_html


class TextNodetoHtmlTest(unittest.TestCase):
    def test_textnode_to_html(self):
        textnode = TextNode(
            "this should be bold html",
            TextType.bold,
        )
        htmlnode = text_node_to_html(textnode)
        self.assertEqual(htmlnode.to_html(), "<b>this should be bold html</b>")
