from typing import List
from textnode import TextNode, TextType
import re


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


def extract_markdown_images(text: str):
    results = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return results


def extract_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
