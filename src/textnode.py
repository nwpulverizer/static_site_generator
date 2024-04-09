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
