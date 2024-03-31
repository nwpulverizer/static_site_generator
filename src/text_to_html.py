from textnode import TextNode
from htmlnode import LeafNode


def text_node_to_html(text_node: TextNode):
    textnodetype = text_node.text_type
    match textnodetype.name:
        case "text":
            return LeafNode(text_node.text, None)
        case "bold":
            return LeafNode(text_node.text, "b")
        case "italic":
            return LeafNode(text_node.text, "i")
        case "code":
            return LeafNode(text_node.text, "code")
        case "link":
            return LeafNode(text_node.text, "a", props={"href": text_node.url})
        case "image":
            return LeafNode(
                "", "img", props={"src": text_node.url, "alt": text_node.text}
            )
