from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    # My solution
    # match text_node.text_type:
    #     case TextType.TEXT:
    #         return LeafNode(tag=None, value=text_node.text, children=None)
    #     case TextType.BOLD:
    #         return LeafNode(tag="b", value=text_node.text, children=None)
    #     case TextType.ITALIC:
    #         return LeafNode(tag="i", value=text_node.text, children=None)
    #     case TextType.CODE:
    #         return LeafNode(tag="code", value=text_node.text, children=None)
    #     case TextType.LINK:
    #         return LeafNode(
    #             tag="a",
    #             value=text_node.text,
    #             children=None,
    #             props={"href": f"{text_node.url}"},
    #         )
    #     case TextType.IMAGE:
    #         return LeafNode(
    #             tag="img",
    #             value="",
    #             children=None,
    #             props={"src": f"{text_node.url}", "alt": f"{text_node.text}"},
    #         )
    #     case _:
    #         return LeafNode(tag=None, value="something is wrong", children=None)
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("invalid URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("invalid URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")
