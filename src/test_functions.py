import unittest

from textnode import TextNode, TextType
from functions import (
    text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, 
    extract_markdown_links, split_nodes_image, split_nodes_link
    )


class TestFunctions(unittest.TestCase):

    def test_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_node_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_to_html_node_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
        
    def test_to_html_node_code(self):
        node = TextNode("This text node displays code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This text node displays code")

    def test_to_html_node_link(self):
        node = TextNode("This is a text node is a link", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node is a link")
        self.assertEqual(html_node.props, {"href": node.url})
        
    def test_to_html_node_image(self):
        node = TextNode("I AM IMAGE DESCRIPTION", TextType.IMAGE, "https://totalyavalidimageurl.somewhere/img.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": node.url, "alt": "I AM IMAGE DESCRIPTION"})

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.PLAIN))
    
    #the following test are not accurate in what the delimiters represent, as ** is the correct delimiter for bold text
    def test_split_nodes_delimiter_stacked_delimiter(self):
        node = TextNode("**test****", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("test", TextType.PLAIN))
    
    def test_split_nodes_delimiter_stacked_delimiter2(self):
        node = TextNode("*one**two****three*", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("one", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode("two", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode("three", TextType.BOLD))

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("*one*two*three*", TextType.PLAIN)
        node2 = TextNode("*from* node two", TextType.PLAIN)
        node3 = TextNode("and **three**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "*", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("one", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode("two", TextType.PLAIN))
        self.assertEqual(new_nodes[2], TextNode("three", TextType.BOLD)) 
        self.assertEqual(new_nodes[3], TextNode("from", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" node two", TextType.PLAIN))
        self.assertEqual(new_nodes[5], TextNode("and ", TextType.PLAIN))
        self.assertEqual(new_nodes[6], TextNode("three", TextType.PLAIN))                

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("**test***", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("test", TextType.BOLD))

    def test_split_nodes_delimiter_none_match(self):
        node = TextNode("**test****", TextType.PLAIN)
        def helper():
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertRaises(Exception, helper)
    
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("this is _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("this is ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))

    def test_split_nodes_delimiter_mixed(self):
        node = TextNode("this is _italic_ and this is **ignored**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("this is ", TextType.PLAIN))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" and this is **ignored**", TextType.PLAIN))
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)") 
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)") 
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_not_links(self):
        matches = extract_markdown_images("[This](https://google.com) is a link!") 
        self.assertListEqual([], matches)

    def test_extract_markdown_links_not_images(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)") 
        self.assertListEqual([], matches)

    def test_extract_markdown_links_not_images_multi(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [this is a link](https://google.com)") 
        self.assertListEqual([("this is a link", "https://google.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://boot.dev)", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boots.dev) and [another link](https://google.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boots.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )



