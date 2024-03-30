import unittest

from htmlnode import HTMLNode, LeafNode


class HTMLNodeTest(unittest.TestCase):
    def test_repr(self):
        node1 = HTMLNode(
            tag="p",
            value="im in a p",
            children=HTMLNode(),
            props={"style": "font-weight:bold"},
        )
        self.assertEqual(
            "HTMLNode(p, im in a p, HTMLNode(None, None, None, None), {'style': 'font-weight:bold'})",
            repr(node1),
        )

    def test_props_to_html(self):
        node1 = HTMLNode(
            tag="p",
            value="im in a p",
            children=HTMLNode(),
            props={"style": "font-weight:bold"},
        )
        self.assertEqual(' style="font-weight:bold"', node1.props_to_html())


class LeafNodeTest(unittest.TestCase):
    def test_nochildren(self):
        leaf = LeafNode("value", tag="p", props={"style": "font-weight:bold"})
        self.assertEqual(leaf.children, None)

    def test_tohtml(self):
        leaf = LeafNode("value", tag="a", props={"href": "https://url.com"})
        self.assertEqual('<a href="https://url.com">value</a>', leaf.to_html())


if __name__ == "__main__":
    unittest.main()
