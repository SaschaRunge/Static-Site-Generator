import unittest

from blocks import BlockType
from blocks import block_to_block_type

class TestBlocks(unittest.TestCase):
    def test_block_is_empty(self):
        md = ""
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_heading_single_hashtag(self):
        md = "# This is a heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING1)

    def test_is_heading_max_hashtags(self):
        md = "###### This is a heading"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING6)

    def test_is_heading_seperated_hashtags(self):
        md = "## # This should be allowed."
        self.assertEqual(block_to_block_type(md), BlockType.HEADING2)
    
    def test_is_heading_to_many_hashtags(self):
        md = "########## This is not a heading"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_heading_to_many_hashtags(self):
        md = "#1231# This is not a heading"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_is_heading_just_text(self):
        md = "This is not a heading"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_is_heading_just_hashtags(self):
        md = "###"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_is_heading_hashtags_with_space(self):
        md = "### "
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_code_block(self):
        md = "```This is a code block.```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_is_code_someone_likes_using_backticks(self):
        md = "````````````This is (unfortunately) code.````````````````"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_is_code_block_missmatch_start_backtick(self):
        md = "``This is not a code block.```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_code_block_missmatch_end_backtick(self):
        md = "```This is not a code block.``"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_is_heading_code_override(self):
        md = "### ```This is still a heading.```"
        self.assertEqual(block_to_block_type(md), BlockType.HEADING3)

    def test_is_heading_broken_code_override(self):
        md = "#a## ```This is neither a heading nor code.```"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_heading_empty(self):
        md = "### "
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_quote_block(self):
        md = ">Line1\n>Line2\n>Line3"
        self.assertEqual(block_to_block_type(md), BlockType.QUOTE)

    def test_is_not_quote_block_added_space_beginning(self):
        md = " >Line1\n>Line2\n>Line3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)
    
    def test_is_not_quote_block_added_space_middle(self):
        md = ">Line1\n >Line2\n>Line3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_quote_block_missing_identifier(self):
        md = ">Line1\nLine2\n>Line3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_unordered_list(self):
        md = "- Line1\n- Line2\n- Line3"
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_is_unordered_list_only_start_char(self):
        md = "- \n- \n- "
        self.assertEqual(block_to_block_type(md), BlockType.UNORDERED_LIST)

    def test_is_unordered_list_missing_space(self):
        md = "- Line1\n-Line2\n- Line3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_ordered_list(self):
        md = "1. Line1\n2. Line2\n3. Line3"
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_is_ordered_list_value_skipped(self):
        md = "1. Line1\n3. Line2\n4. Line3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)

    def test_is_ordered_list_missing_space(self):
        md = "1. Line1\n2.Line2\n3. Line3"
        self.assertEqual(block_to_block_type(md), BlockType.PARAGRAPH)


    




    

               