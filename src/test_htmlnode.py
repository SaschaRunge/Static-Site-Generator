import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        props_string = HTMLNode(None, None, None, props).props_to_html()
        should_be = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(props_string, should_be)

    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        HTMLNode_as_string = str(HTMLNode())
        should_be = "HTMLNode(None, None, None, None)"

        self.assertEqual(HTMLNode_as_string, should_be)

        HTMLNode_as_string = str(HTMLNode("h1", "this is a test", HTMLNode(), props))
        should_be = f'HTMLNode(h1, this is a test, HTMLNode(None, None, None, None), {props})'

        self.assertEqual(HTMLNode_as_string, should_be)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "this is a link", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">this is a link</a>')

    def test_leaf_to_html_multiprops(self):
        props = {
            "href": "https://boot.dev",
            "target": "_blank",
        }

        node = LeafNode("a", "this is another link", props)
        self.assertEqual(node.to_html(), '<a href="https://boot.dev" target="_blank">this is another link</a>')

    def test_leaf_value_error(self):
        def _helper():
            node = LeafNode("p", "this is another test")
            node.value = ""
            node.to_html()
        self.assertRaises(ValueError, _helper)

  





if __name__ == "__main__":
    unittest.main()