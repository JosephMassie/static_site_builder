import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
