from functools import reduce

from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_blocks import *
from build import *

def main():
    md = """### This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

```codeblock **bolded**```

* 1
* 2
* *3*

. 1
.  2
.   3

>*some* **quotes**...
>over here
"""
    node = markdown_to_html_node(md)
    print(node.to_html())

    copy_dir()

if __name__ == "__main__":
    main()
