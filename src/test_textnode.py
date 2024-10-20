import unittest
from functools import reduce

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Image node", TextType.IMAGE, "https://www.google.com")
        node2 = TextNode("Image node", TextType.IMAGE)
        self.assertNotEqual(node, node2)
    
    def test_not_eq_type(self):
        node = TextNode("Image node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("Image node", TextType.IMAGE, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("node", TextType.BOLD, "https://www.google.com")
        node2 = TextNode("Image node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)

class TestSplitDelimiters(unittest.TestCase):
    def test_code(self):
        node = TextNode("some `code` block", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(nodes[1].text_type, TextType.CODE.value)
        self.assertEqual(len(nodes), 3)
    
    def test_bold(self):
        node = TextNode("**bold** text", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes[1].text_type, TextType.BOLD.value)
        self.assertEqual(len(nodes), 3)
    
    def test_multiple_types(self):
        node1 = TextNode("some **bold** text", TextType.TEXT)
        node2 = TextNode("some `code` block", TextType.TEXT)
        nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(len(nodes), 4)

class TestLinkAndImageExtracts(unittest.TestCase):
    def test_image_extract(self):
        text = "some markdown ![alt text](src) \n more text [link text](href) blah blah"
        matches = extract_markdown_images(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], ("alt text", "src"))
    
    def test_link_extract(self):
        text = "some markdown ![alt text](src) \n more text [link text](href) blah blah"
        matches = extract_markdown_links(text)
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0], ("link text", "href"))

class TestTextToNodes(unittest.TestCase):
    def test_main(self):
        text = "`code block` some *markdown* ![alt text](src) more text [link text](href) **blah** blah"
        nodes = text_to_textnodes(text)
        string = reduce(lambda r, tn: r + f"\n{tn}", nodes, "")
        self.assertEqual(len(nodes), 11)
        self.assertEqual(string, """
TextNode(, 0, None)
TextNode(code block, 3, None)
TextNode( some , 0, None)
TextNode(markdown, 2, None)
TextNode( , 0, None)
TextNode(alt text, 5, src)
TextNode( more text , 0, None)
TextNode(link text, 4, href)
TextNode( , 0, None)
TextNode(blah, 1, None)
TextNode( blah, 0, None)""")

if __name__ == "__main__":
    unittest.main()
