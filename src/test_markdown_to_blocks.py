import unittest

from markdown_to_blocks import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_main(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.



* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# This is a heading")

if __name__ == "__main__":
    unittest.main()
