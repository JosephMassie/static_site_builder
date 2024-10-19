from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5

class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str=None) -> None:
        self.text = text
        self.text_type = text_type.value
        self.url = url
    
    def __eq__(self, value: object) -> bool:
        return self.text == value.text and self.text_type == value.text_type and self.url == value.url
    
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL.value:
            return LeafNode(value=text_node.text)
        case TextType.BOLD.value:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC.value:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE.value:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK.value:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE.value:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid TextType for text_node {text_node.text_type}")