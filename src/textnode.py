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
        if node.text_type.name != "text":
            new_nodes.append(node)
        elif text_type.name != "link" or text_type.name != "image":
            # this will probably not work for image types right?
            # image is ![alt text](image.url)
            # I could split on ![ so that I make sure
            # I am not just hitting a exclamation point.
            split_text = node.text.split(delimiter)
            # the even indexes will always be the text nodes.
            updated_nodes = []
            for i, splited in enumerate(split_text):
                if i % 2 == 0:
                    updated_nodes.append(TextNode(splited, TextType.text))
                else:
                    updated_nodes.append(TextNode(splited, text_type))
            new_nodes.extend(updated_nodes)
        # elif text_type.name == "link":
        # do the things for link markdown

        # elif text_type.name == "image":
        # do the thing for image markdown
        # in this case my delimitter will be ![
        # example: text with image ![alt](image.jpg)
        # split on ![: text with image, alt](image.jpg)
        #  first part will be text
        #  second part need to split ] to get alt,
        #  then on ) and lstrip ( to get image url

        return new_nodes
