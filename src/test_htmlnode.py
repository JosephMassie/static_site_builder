import unittest

from htmlnode import HTMLNode

class HTMLNodeTests(unittest.TestCase):
    def test_str_out(self):
        node = HTMLNode("div", "some str")
        target = """HTML Node : tag=div value=some str

no children

props:"""
        self.assertEqual(f"{node}", target)
    
    def test_str_out_children(self):
        child = HTMLNode("child")
        parent = HTMLNode(children=[child])
        target ="HTML Node : tag=None value=None\n------\nchildren:\nHTML Node : tag=child value=None\n\nno children\n\nprops:\n------\nprops:"
        self.assertEqual(f"{parent}", target)

    
    def test_props_str_out(self):
        node = HTMLNode(props={"action": "false", "alt": "some str"})
        target = " action=false alt=some str"
        self.assertEqual(node.props_to_html(), target)

if __name__ == "__main__":
    unittest.main()
