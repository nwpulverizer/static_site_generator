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


def split_nodes_images(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if extracted_images == []:
            new_nodes.append(node)
        else:
            count = 0
            while count < len(extracted_images):
                imagetup = extracted_images[count]
                split_string = f"![{imagetup[0]}]({imagetup[1]})"
                new_text_nodes = node.text.split(split_string, 1)
                firstitem = TextNode(new_text_nodes[0], TextType.text)
                node = TextNode(new_text_nodes[1], TextType.text)
                image_node = TextNode(imagetup[0], TextType.image, imagetup[1])
                new_nodes.extend([firstitem, image_node])
                count += 1
            new_nodes.append(node)
            for node in new_nodes:
                if node.text == "":
                    new_nodes.remove(node)
            print(new_nodes)
    return new_nodes


def split_nodes_links(old_nodes: List[TextNode]):
    new_nodes = []
    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if extracted_links == []:
            new_nodes.append(node)
        else:
            count = 0
            while count < len(extracted_links):
                linktup = extracted_links[count]
                split_string = f"![{linktup[0]}]({linktup[1]})"
                new_text_nodes = node.text.split(split_string, 1)
                firstitem = TextNode(new_text_nodes[0], TextType.text)
                node = TextNode(new_text_nodes[1], TextType.text)
                link_node = TextNode(linktup[0], TextType.link, linktup[1])
                new_nodes.extend([firstitem, link_node])
                count += 1
            new_nodes.append(node)
            for node in new_nodes:
                if node.text == "":
                    new_nodes.remove(node)
            print(new_nodes)
    return new_nodes
