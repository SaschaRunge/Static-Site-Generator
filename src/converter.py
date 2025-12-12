from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(node: LeafNode):
    match(node.text_type):
        case TextType.PLAIN:
            return LeafNode(None, node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINK:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {
                "src": node.url,
                "alt": node.text})