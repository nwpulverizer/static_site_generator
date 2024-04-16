from typing import Optional, Union, List, ForwardRef


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list] = None,
        props: Optional[dict] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        htmlstr = ""
        for k, v in self.props.items():
            htmlstr += f' {k}="{v}"'
        return htmlstr

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: Union[str, None], props: Optional[dict] = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


ParentNode = ForwardRef(
    "ParentNode",
)


class ParentNode(HTMLNode):
    def __init__(
        self,
        children: List[Union[LeafNode, ParentNode]],
        tag: Optional[str] = None,
        props: Optional[dict] = None,
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        """
        Reads in the tag attribute and outputs a string of html
        for that tag. Calls on children as well.
        """
        if self.tag is None:
            raise ValueError("Parent requires a tag")
        if self.children is None:
            raise ValueError("Parent requires children")
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
