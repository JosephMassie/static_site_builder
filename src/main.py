from functools import reduce

from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    #t_node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
    #print(t_node)
    #child = HTMLNode(tag="child", value="foo bar", props={"test": "true"})
    #html_node = HTMLNode(tag="div", children=[child], props={"action": "false"})
    #print(html_node)

    #child1 = LeafNode(value="str")
    #child2 = LeafNode(tag="child", value="foo bar")
    #parent = ParentNode(tag="div", children=[child1, child2])
    #print(f"\nNew Node\n{parent.to_html()}")

    #leaf = LeafNode(value="plain text", props={"href": "some url"})
    #leaf_tag = LeafNode(tag="p", value="para", props={"style": "font-weight:bold;"})
    #print(f"\n{leaf.to_html()}")
    #print(f"\n{leaf_tag.to_html()}")

    #link = text_node_to_html_node(t_node)
    #print(f"\n\nlink: {link.to_html()}")

    # test_nodes = [
    #     TextNode("testing 1 `2` 3...", TextType.TEXT),
    #     TextNode("`code block`", TextType.TEXT),
    #     TextNode("**bold** text", TextType.TEXT),
    #     TextNode("*text* italic", TextType.TEXT)
    # ]
    # test_nodes = split_nodes_delimiter(test_nodes, "`", TextType.CODE)
    # test_nodes = split_nodes_delimiter(test_nodes, "**", TextType.BOLD)
    # test_nodes = split_nodes_delimiter(test_nodes, "*", TextType.ITALIC)

    # string = reduce(lambda r, tn: r + f"\n{tn}", test_nodes, "\n---\nparsed\n")
    # print(string)

    text = "some markdown ![alt text](src) more text [link text](href) blah blah"
    node = TextNode(text, TextType.TEXT)
    updated_nodes = split_nodes_link([node])
    updated_nodes = split_nodes_image(updated_nodes)
    string = reduce(lambda r, tn: r + f"\n{tn}", updated_nodes, "\n---\nparsed\n")
    print(string)

if __name__ == "__main__":
    main()
