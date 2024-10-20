import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = 0
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
        case TextType.TEXT.value:
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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    def map_blocks(blocks: list[str], i=0) -> list[TextNode]:
        if i >= len(blocks):
            return None

        block = blocks[i]
        if (i + 1) % 2 == 0:
            node = TextNode(block, text_type)
        else:
            node = TextNode(block, TextType.TEXT)

        nodes = [node]
        add_nodes = map_blocks(blocks, i + 1)
        if add_nodes != None:
            nodes.extend(add_nodes)

        return nodes

    for node in old_nodes:
        delim_count = node.text.count(delimiter)
        if node.text_type != TextType.TEXT.value or delim_count == 0:
            new_nodes.append(node)
        elif delim_count % 2 != 0:
            raise Exception("invalid markdown syntax all delimiters must be paired")
        else:
            blocks = node.text.split(delimiter);
            nodes = map_blocks(blocks)
            new_nodes.extend(nodes)
    return new_nodes

def extract_markdown_images(text: str):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if node.text_type != TextType.TEXT.value or len(matches) == 0:
            new_nodes.append(node)
        else:
            text = node.text
            for i in range(len(matches)):
                alt, src = matches[i]
                sections = text.split(f"![{alt}]({src})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, src))
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def extract_markdown_links(text: str):
    matches = re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if node.text_type != TextType.TEXT.value or len(matches) == 0:
            new_nodes.append(node)
        else:
            text = node.text
            for i in range(len(matches)):
                alt, src = matches[i]
                sections = text.split(f"[{alt}]({src})", 1)
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.LINK, src))
                text = sections[1]
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = [
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
    ]

    nodes = [TextNode(text, TextType.TEXT)]
    for (delimiter, text_type) in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
