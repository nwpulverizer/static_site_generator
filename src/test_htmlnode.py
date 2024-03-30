import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class ParentNodeTest(unittest.TestCase):
    def test_tohtml_noprops(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("Bold Text", "b"),
                LeafNode("Plain ol' text", None),
                LeafNode("italic/spicy txt", "i"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold Text</b>Plain ol' text<i>italic/spicy txt</i></p>",
            node.to_html(),
        )

    def test_tohtml_props(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("Bold Text", "b"),
                LeafNode("Plain old text", None),
                LeafNode("italic/spicy txt", "i"),
            ],
            props={"style": "color:blue"},
        )
        self.assertEqual(
            '<p style="color:blue"><b>Bold Text</b>Plain old text<i>italic/spicy txt</i></p>',
            node.to_html(),
        )

    def test_tohtml_single_nested_parents(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("Bold Text", "b"),
                LeafNode("Plain old text", None),
                LeafNode("italic/spicy txt", "i"),
            ],
            props={"style": "color:blue"},
        )
        node2 = ParentNode(tag="div", children=[node])
        self.assertEqual(
            '<div><p style="color:blue"><b>Bold Text</b>Plain old text<i>italic/spicy txt</i></p></div>',
            node2.to_html(),
        )

    def test_tohtml_double_nested_parents(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("Bold Text", "b"),
                LeafNode("Plain old text", None),
                LeafNode("italic/spicy txt", "i"),
            ],
            props={"style": "color:blue"},
        )
        node2 = ParentNode(tag="div", children=[node])
        node3 = ParentNode(tag="div", children=[node2])
        self.assertEqual(
            '<div><div><p style="color:blue"><b>Bold Text</b>Plain old text<i>italic/spicy txt</i></p></div></div>',
            node3.to_html(),
        )

    def test_tohtml_nochildren(self):
        node = ParentNode(tag="div", children=None)
        self.assertRaises(ValueError, node.to_html)

    def test_tohtml_notag(self):
        node = ParentNode(tag=None, children=[LeafNode("Bold text", "b")])
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
