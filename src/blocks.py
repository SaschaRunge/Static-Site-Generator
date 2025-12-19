from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING1 = "h1"
    HEADING2 = "h2"
    HEADING3 = "h3"
    HEADING4 = "h4"
    HEADING5 = "h5"
    HEADING6 = "h6"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "li"
    ORDERED_LIST = "ol"

def block_to_block_type(md_text):

    if not md_text:
        return BlockType.PARAGRAPH
    
    is_heading_len = is_heading(md_text)
    if is_heading_len == 1:
        return BlockType.HEADING1
    if is_heading_len == 2:
        return BlockType.HEADING2
    if is_heading_len == 3:
        return BlockType.HEADING3
    if is_heading_len == 4:
        return BlockType.HEADING4
    if is_heading_len == 5:
        return BlockType.HEADING5
    if is_heading_len == 6:
        return BlockType.HEADING6
    
    if is_code_block(md_text):
        return BlockType.CODE
    
    if is_quote_block(md_text):
        return BlockType.QUOTE
    
    if is_unordered_list(md_text):
        return BlockType.UNORDERED_LIST
    
    if is_ordered_list(md_text):
        return BlockType.ORDERED_LIST
            
    return BlockType.PARAGRAPH
    
def is_heading(md_text):
    text_parts = md_text.split(" ", 1)
    if len(text_parts) > 1:
        if text_parts[0] and text_parts[0] in "######" and text_parts[1]: # a bit unclear if empty headings allowed. Disallow for now
            return len(text_parts[0])
    return False

def is_code_block(md_text):
    if len(md_text) > 6:
        if (md_text[:3] == "```" and md_text[-3:] == "```"):
            return True
    return False

def is_quote_block(md_text):
    text_parts = md_text.split("\n")
    for text_part in text_parts:
        if not text_part or text_part[0] != ">":
            return False
    return True
                
def is_unordered_list(md_text):
    text_parts = md_text.split("\n")
    for text_part in text_parts:
        if not text_part or text_part[0:2] != "- ":
            return False
    return True

def is_ordered_list(md_text):
    text_parts = md_text.split("\n")
    line_count = 1
    for text_part in text_parts:
        if len(text_part) < 3 or text_part[0:3] != f"{line_count}. ":
            return False
        line_count += 1
    return True


