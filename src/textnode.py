from typing import Optional, List
from enum import Enum


class TextType(Enum):
    text = 1
    bold = 2
    italic = 3
    code = 4
    link = 5
    image = 6


class TextNode:
    def __init__(
        self, TEXT: str, TEXT_TYPE: TextType, URL: Optional[str] = None
    ) -> None:
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    # markdown specifies the deliminter and text type - as in
    # if the delimiter is `, then it is code text type. Why do we need
    # to have text_type also?
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text:
            new_nodes.append(node)
        elif text_type.name != "link" or text_type.name != "image":
            split_text = node.text.split(delimiter)
            # the even indexes will always be the text nodes.
            updated_nodes = []
            for i, splited in enumerate(split_text):
                if i % 2 == 0:
                    updated_nodes.append(TextNode(splited, TextType.text))
                else:
                    updated_nodes.append(TextNode(splited, text_type))
            new_nodes.extend(updated_nodes)
        for item in new_nodes:
            if item.text_type == TextType.text and item.text == "":
                new_nodes.remove(item)
        return new_nodes
