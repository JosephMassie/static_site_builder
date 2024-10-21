from functools import reduce

from textnode import *
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_to_blocks import *
from build import *

def main():
    copy_dir()
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()
