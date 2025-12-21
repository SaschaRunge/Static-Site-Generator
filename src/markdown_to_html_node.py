from functions import markdown_to_blocks, text_to_textnodes, text_node_to_html_node
from blocks import BlockType, block_to_block_type
from htmlnode import ParentNode
from textnode import TextNode, TextType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    parent_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes = text_to_child_nodes(block, block_type)
        #if block_type == BlockType.QUOTE:
            #child_nodes = [ParentNode("p", child_nodes)]  
        if block_type == BlockType.UNORDERED_LIST:
            parent_nodes.append(ParentNode("ul", child_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            parent_nodes.append(ParentNode("ol", child_nodes))
        else: 
            if block_type == BlockType.CODE:
                temp_node = ParentNode(block_type.value, child_nodes)
                parent_nodes.append(ParentNode("pre", [temp_node]))
            else:
                parent_nodes.append(ParentNode(block_type.value, child_nodes))                
    return ParentNode("div", parent_nodes) 

def text_to_child_nodes(text, parent_block_type) -> list:
    match(parent_block_type):
        case BlockType.CODE:
            text_nodes = code_block_to_text_nodes(text)
        case BlockType.HEADING1:
            text_nodes = heading_to_text_nodes(text)
        case BlockType.HEADING2:
            text_nodes = heading_to_text_nodes(text) 
        case BlockType.HEADING3:
            text_nodes = heading_to_text_nodes(text) 
        case BlockType.HEADING4:
            text_nodes = heading_to_text_nodes(text) 
        case BlockType.HEADING5:
            text_nodes = heading_to_text_nodes(text) 
        case BlockType.HEADING6:
            text_nodes = heading_to_text_nodes(text)  
        case BlockType.QUOTE:
            text_nodes = quote_to_text_nodes(text) 
        case BlockType.UNORDERED_LIST:
            list_of_text_nodes = list_to_list_of_text_nodes(text)         
        case BlockType.ORDERED_LIST:
            list_of_text_nodes = list_to_list_of_text_nodes(text) 
        case _:
            text_nodes = text_to_textnodes(text)

    html_nodes = []
    if parent_block_type != BlockType.UNORDERED_LIST and parent_block_type != BlockType.ORDERED_LIST:
        for text_node in text_nodes:
            html_node = text_node_to_html_node(text_node)
            html_nodes.append(html_node)
    else:
        temp_nodes = []
        for text_nodes in list_of_text_nodes:
            for text_node in text_nodes:
                temp_node = text_node_to_html_node(text_node)
                temp_nodes.append(temp_node)
            html_nodes.append(ParentNode("li", temp_nodes))
            temp_nodes = [] 
    return html_nodes

def code_block_to_text_nodes(text):
    return [TextNode(text[3:-3].strip() + "\n", TextType.TEXT)]

def heading_to_text_nodes(text):
    text_parts = text.strip().split(" ", 1)
    return text_to_textnodes(text_parts[1])

def quote_to_text_nodes(text):
    text_parts = text.split("\n")
    parsed_text = []
    for text_part in text_parts:
        if text_part:
            text_part = text_part[1:].strip()
            text_part += " "
            parsed_text.append(text_part)
    return text_to_textnodes("".join(parsed_text).strip())

def list_to_list_of_text_nodes(text):
    text_parts = text.split("\n")
    list_of_text_nodes = []
    for text_part in text_parts:
        if text_part:
            text_part = text_part.split(" ", 1)[1].strip()
            list_of_text_nodes.append(text_to_textnodes(text_part))
    return list_of_text_nodes




