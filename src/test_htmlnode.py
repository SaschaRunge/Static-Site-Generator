import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
            node.value = None
            node.to_html()
        self.assertRaises(ValueError, _helper)

    #probably not a correct way to handle <img> -> See void elements
    def test_leaf_empty_string_value(self):
        node = LeafNode("img", "")
        self.assertEqual(node.to_html(), "<img></img>")
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "this is yet another test")
        self.assertEqual(node.to_html(), "this is yet another test")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    # <img> and <br> tags are handled like any other tag for now, likely not correct html but it will do as a test for now
    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode("br", "")
        child_node = ParentNode("img", [grandchild_node], {
            "src": "smiley.gif",
            "alt": "HTML tutorial", 
            "style": "width:42px;height:42px;"
        })
        parent_node = ParentNode("a", [child_node], {"href": "default.asp"})
        self.assertEqual(
            parent_node.to_html(),
            '<a href="default.asp"><img src="smiley.gif" alt="HTML tutorial" style="width:42px;height:42px;"><br></br></img></a>',
        )

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("b", "i am bold")
        child_node2 = LeafNode("i", "i am italic")
        child_node3 = LeafNode("blockquote", "i am a quote")
        children = [child_node1, child_node2, child_node3]
        parent_node = ParentNode("p", children)
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>i am bold</b><i>i am italic</i><blockquote>i am a quote</blockquote></p>",
        )

    def test_to_html_with_multiple_children_and_grandchildren(self):
        children1 = [LeafNode("b", "i am bold"), LeafNode("i", "i am italic"), LeafNode("blockquote", "i am a quote")]
        children2 = [LeafNode("li", "i am a list entry"), LeafNode("li", "me too"), LeafNode("li", "dito")]
        parent_node2 = ParentNode("span", [ParentNode("div", children1)])
        parent_node3 = ParentNode("ol", children2)
        parent_node4 = ParentNode("p", [parent_node2, parent_node3])
        self.assertEqual(
            parent_node4.to_html(),
            "<p><span><div>"
            "<b>i am bold</b><i>i am italic</i><blockquote>i am a quote</blockquote>"
            "</div></span>"
            "<ol>"
            "<li>i am a list entry</li>"
            "<li>me too</li>"
            "<li>dito</li>" 
            "</ol></p>",
        )

    def test_parent_has_no_children(self):
        def _helper():
            ParentNode("p", []).to_html()
        self.assertRaises(ValueError, _helper)
    
    def test_parent_has_no_tag(self):
        def _helper():
            ParentNode("", [LeafNode("b", "i am bold")]).to_html()
        self.assertRaises(ValueError, _helper)




if __name__ == "__main__":
    unittest.main()