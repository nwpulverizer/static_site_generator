import unittest

from textnode import TextNode


class TextNodeTest(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_ne(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold1")
        self.assertNotEqual(node1, node2)

    def test_emptystrurl(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "")
        self.assertNotEqual(node1, node2)

    def test_fullurl_eq(self):
        node1 = TextNode("This is a text node", "bold", "http://url.com")
        node2 = TextNode("This is a text node", "bold", "http://url.com")
        self.assertEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()