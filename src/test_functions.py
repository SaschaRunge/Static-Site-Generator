import unittest

from textnode import TextNode, TextType
from functions import (
    text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, 
    extract_markdown_links, split_nodes_image, split_nodes_link,
    text_to_textnodes, markdown_to_blocks
    )


class TestFunctions(unittest.TestCase):

    def test_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
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
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))
    
    #the following test are not accurate in what the delimiters represent, as ** is the correct delimiter for bold text
    def test_split_nodes_delimiter_stacked_delimiter(self):
        node = TextNode("**test****", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("test", TextType.TEXT))
    
    def test_split_nodes_delimiter_stacked_delimiter2(self):
        node = TextNode("*one**two****three*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("one", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode("two", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode("three", TextType.BOLD))

    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("*one*two*three*", TextType.TEXT)
        node2 = TextNode("*from* node two", TextType.TEXT)
        node3 = TextNode("and **three**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "*", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("one", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode("two", TextType.TEXT))
        self.assertEqual(new_nodes[2], TextNode("three", TextType.BOLD)) 
        self.assertEqual(new_nodes[3], TextNode("from", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" node two", TextType.TEXT))
        self.assertEqual(new_nodes[5], TextNode("and ", TextType.TEXT))
        self.assertEqual(new_nodes[6], TextNode("three", TextType.TEXT))                

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("**test***", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("test", TextType.BOLD))
    
    def test_split_nodes_delimiter_no_matching_text(self):
        node = TextNode("test", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("test", TextType.TEXT))

    def test_split_nodes_delimiter_none_match(self):
        node = TextNode("**test****", TextType.TEXT)
        def helper():
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertRaises(Exception, helper)
    
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("this is _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))

    def test_split_nodes_delimiter_mixed(self):
        node = TextNode("this is _italic_ and this is **ignored**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("this is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" and this is **ignored**", TextType.TEXT))
    
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
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_just_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)![third image](https://i.imgur.com/uYsVb2Q.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("third image", TextType.IMAGE, "https://i.imgur.com/uYsVb2Q.jpeg"),
            ],
            new_nodes,
        )

    def test_split_single_image_multiple_times(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)![image3](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image3", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_plain_text(self):
        node = TextNode(
            "This is text with noooo images, no images at all.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with noooo images, no images at all.", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_plain_text_as_type_image(self):
        node = TextNode(
            "This is text with noooo images, no images at all.",
            TextType.IMAGE,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boots.dev) and [another link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boots.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )
    
    def test_split_multiple_nodes_of_same_type(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a ![third image](https://i.imgur.com/uYsVb2Q.jpeg) added.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("third image", TextType.IMAGE, "https://i.imgur.com/uYsVb2Q.jpeg"),
                TextNode(" added.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_iterations(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_multiple_nodes_of_different_type(self):
        image_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        link_node = TextNode(
            "This is text with a [link](https://boots.dev) and [another link](https://google.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([image_node, link_node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boots.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://google.com"),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
    
    def test_text_to_textnodes_order_shuffled(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) is not a [link](https://boot.dev) and this _italic_ **text** has a `code block`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" is not a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and this ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),                
            ],
            nodes,
        )

    def test_text_to_textnodes_order_shuffled_with_multiple_links(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) is not a [link](https://boot.dev) and [another link](https://google.com) and this _italic_ **text** has a `code block`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" is not a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://google.com"),
                TextNode(" and this ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" has a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),                
            ],
            nodes,
        )

    def test_text_to_textnodes_single(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),             
            ],
            nodes,
        )
    
    def test_text_to_textnodes_nothing(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual([], nodes)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_strip_redundant_newline(self):
        md = """
This is **bolded** paragraph






This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items



+1
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "+1",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\n"
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
            ],
        )

    def test_markdown_to_blocks_trailing_and_leading_newline(self):
        md = """




This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line








"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\n"
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_newline_only(self):
        md = "\n\n\n\n\n\n\n\n\n"

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_whitespace_only_block(self):
        md = """
This is **bolded** paragraph

               

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

        
    


