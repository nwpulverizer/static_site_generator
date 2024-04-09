# define block as something split by a single blank line.
# True for well behaved md.
def markdown_to_blocks(markdown: str):
    # based on our simple definition, splitting on \n\n will give us
    # what we want
    split = markdown.split("\n\n")
    non_empty = filter(lambda x: x != "")
    return split
