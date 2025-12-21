import unittest

from markdown_to_html_node import markdown_to_html_node

class TestBlocks(unittest.TestCase):
    maxDiff = None

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_nested_unresolved_inlines_in_paragraphs(self):
        md = """
This is **bolded and _non italic_ tesxt.**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded and _non italic_ tesxt.</b></p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_codeblock_missing_backtick(self):
        md = """
``
This is text that _should not_ remain
the **same** even with inline stuff
````
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p> This is text that <i>should not</i> remain the <b>same</b> even with inline stuff </p></div>",
        )

    def test_headings(self):
        md = """
### This is a heading with _italic_ and
some **bold** text.

#### This is an additional heading.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading with <i>italic</i> and some <b>bold</b> text.</h3><h4>This is an additional heading.</h4></div>",
        )

    def test_quotes(self):
        md = """
>   These are quotes with _italic_ text.
> And **bold** text.
>And a bit of `code`.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>These are quotes with <i>italic</i> text. And <b>bold</b> text. And a bit of <code>code</code>.</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
-   These are quotes with _italic_ text.
- And **bold** text.
- And a bit of `code`.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>These are quotes with <i>italic</i> text.</li><li>And <b>bold</b> text.</li><li>And a bit of <code>code</code>.</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1.   These are quotes with _italic_ text.
2. And **bold** text.
3. And a bit of `code`.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>These are quotes with <i>italic</i> text.</li><li>And <b>bold</b> text.</li><li>And a bit of <code>code</code>.</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
>   These are quotes with _italic_ text.
> And **bold** text.
>And a bit of `code`.

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>These are quotes with <i>italic</i> text. And <b>bold</b> text. And a bit of <code>code</code>.</blockquote>"
            "<pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
