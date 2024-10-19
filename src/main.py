from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

print("hello world!")

def main():
    t_node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
    print(t_node)
    child = HTMLNode(tag="child", value="foo bar", props={"test": "true"})
    html_node = HTMLNode(tag="div", children=[child], props={"action": "false"})
    print(html_node)

    child1 = LeafNode(value="str")
    child2 = LeafNode(tag="child", value="foo bar")
    parent = ParentNode(tag="div", children=[child1, child2])
    print(f"\nNew Node\n{parent.to_html()}")

    leaf = LeafNode(value="plain text", props={"href": "some url"})
    leaf_tag = LeafNode(tag="p", value="para", props={"style": "font-weight:bold;"})
    print(f"\n{leaf.to_html()}")
    print(f"\n{leaf_tag.to_html()}")

    link = text_node_to_html_node(t_node)
    print(f"\n\nlink: {link.to_html()}")

if __name__ == "__main__":
    main()
