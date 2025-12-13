import re

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

def split_nodes_image(old_nodes):
    return split_nodes_image_or_link(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes_image_or_link(old_nodes, TextType.LINK)

def split_nodes_image_or_link(old_nodes, text_type):
    if not (text_type == TextType.IMAGE or text_type == TextType.LINK):
        raise ValueError("Node is neither an image nor a link.")
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        if text_type == TextType.IMAGE:
            parts = extract_markdown_images(node.text)
            leading_char = "!"
        else:
            parts = extract_markdown_links(node.text)
            leading_char = ""

        node_text = node.text
        for part in parts:
            text, url = part
            delimiter = f"{leading_char}[{text}]({url})"

            if node_text == delimiter:
                break

            text_parts = node_text.split(delimiter, 1)
            if len(text_parts) < 2:
                return ValueError("TextNode does not contain the extracted image/link string.")
            if text_parts[0]:
                new_nodes.append(TextNode(text_parts[0], TextType.PLAIN))
            new_nodes.append(TextNode(text, text_type, url))
            if text_parts[1]:
                node_text = text_parts[1]
            else:
                break

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text) #!\[(.*?)\]\((.*?)\) fails to nested brackets [ []]

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text) #(?<!\!)\[(.*?)\]\((.*?)\) fails, same reason


