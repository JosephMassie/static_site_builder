from textnode import TextNode, TextType
from htmlnode import HTMLNode

print("hello world!")

def main():
    t_node = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev")
    print(t_node)
    child = HTMLNode("child", "foo bar", props={"test": "true"})
    html_node = HTMLNode("div", children=[child], props={"action": "false"})
    print(html_node)
    child2 = HTMLNode("child")
    parent = HTMLNode(children=[child2])
    print(f"\nNew Node\n{parent}")

if __name__ == "__main__":
    main()
