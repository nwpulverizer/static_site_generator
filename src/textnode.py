class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None) -> None:
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
        return repr(f"TextNode: {self.text}, {self.text_type}, {self.url}")
