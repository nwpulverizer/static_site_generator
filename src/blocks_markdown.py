from enum import Enum
import re


class BlockType(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6


# define block as something split by a single blank line.
# True for well behaved md.
def markdown_to_blocks(markdown: str):
    # remove empty new lines from start and end
    markdown = markdown.strip("\n")
    # split on new lines
    split = markdown.split("\n\n")
    # remove empty strings and strip of newline characters in the case
    # of an odd number of empty lines. Also removes leading and trailing whitespaces
    # from individual lines
    non_empty = [x.lstrip("\n").strip() for x in split if x != ""]
    return non_empty


def block_to_block_type(block: str):
    # if you want to consider something a heading even without any text,
    # remove the .* part of the pattern
    if re.match(r"^#{1,6}\s.*", block):
        return BlockType.heading
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    if len(re.findall(r"^>", block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.quote
    if len(re.findall(r"^[*-]", block, re.MULTILINE)) == len(block.split("\n")):
        return BlockType.unordered_list
    if len(re.findall(r"^\d+\.", block, re.MULTILINE)) == len(block.split("\n")):
        lines = block.split("\n")
        number = 1
        # make sure we start with 1 and increment each time, otherwise
        # just a p.
        for line in lines:
            if line.startswith(str(number)):
                number += 1
            else:
                return BlockType.paragraph
        return BlockType.ordered_list
    else:
        return BlockType.paragraph
