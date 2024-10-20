import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class HTMLNodeTests(unittest.TestCase):
    def test_str_out(self):
        node = HTMLNode(tag="div", value="some str")
        target = """HTML Node : tag=div value=some str

no children

props:"""
        self.assertEqual(f"{node}", target)
    
    def test_str_out_children(self):
        child = HTMLNode(tag="child")
        parent = HTMLNode(children=[child])
        target ="HTML Node : tag=None value=None\n------\nchildren:\nHTML Node : tag=child value=None\n\nno children\n\nprops:\n------\nprops:"
        self.assertEqual(f"{parent}", target)

    
    def test_props_str_out(self):
        node = HTMLNode(props={"action": "false", "alt": "some str"})
        target = ' action="false" alt="some str"'
        self.assertEqual(node.props_to_html(), target)

class LeafNodeTests(unittest.TestCase):
    def test_to_html(self):
        leaf = LeafNode(value="plain text")
        self.assertEqual(leaf.to_html(), "plain text")
    
    def test_do_not_render_props_without_tag(self):
        leaf = LeafNode(value="plain text", props={"href": "some url"})
        self.assertEqual(leaf.to_html(), "plain text")
    
    def test_to_html_tag(self):
        leaf_tag = LeafNode(tag="p", value="para", props={"style": "font-weight:bold;"})
        self.assertEqual(leaf_tag.to_html(), '<p style="font-weight:bold;">para</p>')

class ParentNodeTests(unittest.TestCase):
    def test_require_children(self):
        with self.assertRaises(TypeError):
            ParentNode(tag="div")

    def test_require_tag(self):
        with self.assertRaises(TypeError):
            ParentNode()
    
    def test_creates_html_with_children(self):
        child = LeafNode(value="foo")
        child_w_tag = LeafNode(tag="p", value="bar")
        parent = ParentNode(tag="div", children=[child, child_w_tag])
        self.assertEqual(parent.to_html(), "<div>foo<p>bar</p></div>")

if __name__ == "__main__":
    unittest.main()
