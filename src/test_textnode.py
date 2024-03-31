import unittest

from textnode import TextNode, TextType


class TextNodeTest(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node1, node2)

    def test_ne(self):
        node1 = TextNode("This is a text node but different", TextType.text)
        node2 = TextNode("This is a text node", TextType.text)
        self.assertNotEqual(node1, node2)

    def test_emptystrurl(self):
        node1 = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold, "")
        self.assertNotEqual(node1, node2)

    def test_fullurl_eq(self):
        node1 = TextNode("This is a text node", TextType.bold, "http://url.com")
        node2 = TextNode("This is a text node", TextType.bold, "http://url.com")
        self.assertEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.bold, "http://url.com")
        self.assertEqual(
            "TextNode(This is a text node, bold, http://url.com)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
