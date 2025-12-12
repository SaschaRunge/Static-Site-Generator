import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_neq(self):     
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        repr_string = str(TextNode("This is a text node", TextType.BOLD))
        should_be = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr_string, should_be)

        repr_string = str(TextNode("This is a text node", TextType.LINK, "https://boot.dev"))
        should_be = "TextNode(This is a text node, link, https://boot.dev)"
        self.assertEqual(repr_string, should_be)

    def test_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_to_html_node_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        
    def test_to_html_node_code(self):
        node = TextNode("This text node displays code", TextType.CODE)
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This text node displays code")

    def test_to_html_node_link(self):
        node = TextNode("This is a text node is a link", TextType.LINK, "https://google.com")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node is a link")
        self.assertEqual(html_node.props, {"href": node.url})
        
    def test_to_html_node_image(self):
        node = TextNode("I AM IMAGE DESCRIPTION", TextType.IMAGE, "https://totalyavalidimageurl.somewhere/img.jpg")
        html_node = node.to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": "I AM IMAGE DESCRIPTION"})






if __name__ == "__main__":
    unittest.main()