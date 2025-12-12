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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        
        text_parts = node.text.split(delimiter)

        if len(text_parts) % 2 == 0:
            raise Exception(f"TextNode {node} contains invalid Markdown syntax.")
        
        for i in range(len(text_parts)):
            if text_parts[i]:
                is_even = (i % 2 == 0)
                if is_even:
                    new_nodes.append(TextNode(text_parts[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(text_parts[i], text_type))
    return new_nodes


