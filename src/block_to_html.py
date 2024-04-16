from typing import Union
import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import (
    string_to_TextNode,
)
from text_to_html import (
    text_node_to_html,
)
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType


def paragraph_to_html(block: str) -> Union[LeafNode, ParentNode]:
    children = string_to_TextNode(block)
    children = [text_node_to_html(i) for i in children]
    if len(children) > 1:
        return ParentNode(children, "p")
    return children[0]


def heading_to_html(block: str) -> Union[LeafNode, ParentNode]:
    heading_type = 0
    for i in block[:6]:
        if i == "#":
            heading_type += 1
        else:
            break
    cleaned = block.strip("#" * heading_type).strip()
    children = string_to_TextNode(cleaned)
    children = [text_node_to_html(i) for i in children]
    if len(children) > 1:
        return ParentNode(children, f"h{heading_type}")
    else:
        return LeafNode(children[0].value, f"h{heading_type}")


def code_to_html(block: str):
    # not going to check for other md nodes within a code block, because
    # it is fully enclosed
    block = block.strip("```").strip()
    return ParentNode([LeafNode(block, "code")], "pre")


def quote_to_html(block):
    # not going to check for other nodes here either, quotes shouldn't have
    # other nodes in them I think.
    block = block.replace(">", "")
    return LeafNode(block, "blockquote")


def unordered_list_to_html(block):
    block = block.split("\n")
    block = [re.sub(r"^[\*\-]", "", i) for i in block]
    li_children = []
    for item in block:
        item = item.strip()
        item_children = string_to_TextNode(item)
        item_children = [text_node_to_html(i) for i in item_children]
        if len(item_children) > 1:
            li_children.append(ParentNode(item_children, "li"))
        else:
            li_children.append(LeafNode(item_children[0].to_html(), "li"))
    return ParentNode(li_children, "ul")


def ordered_list_to_html(block):
    block = block.split("\n")
    block = [re.sub(r"^\d+\.", "", i) for i in block]
    li_children = []
    for item in block:
        item = item.strip()
        item_children = string_to_TextNode(item)
        item_children = [text_node_to_html(i) for i in item_children]
        if len(item_children) > 1:
            li_children.append(ParentNode(item_children, "li"))
        else:
            li_children.append(LeafNode(item_children[0].to_html(), "li"))
    return ParentNode(li_children, "ol")


def markdown_to_htmlnodes(md_string: str):
    blocks = markdown_to_blocks(md_string)
    html_nodes = []
    for block in blocks:
        blocktype = block_to_block_type(block)
        match blocktype:
            case BlockType.paragraph:
                html_nodes.append(paragraph_to_html(block))
            case BlockType.heading:
                html_nodes.append(heading_to_html(block))
            case BlockType.code:
                html_nodes.append(code_to_html(block))
            case BlockType.quote:
                html_nodes.append(quote_to_html(block))
            case BlockType.unordered_list:
                html_nodes.append(unordered_list_to_html(block))
            case BlockType.ordered_list:
                html_nodes.append(ordered_list_to_html(block))
    return ParentNode(html_nodes, "div")

