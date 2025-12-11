class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_string = ""
        for key, value in self.props.items():
            html_string += f" {key}=\"{value}\""
        return html_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if not value:
            raise ValueError(f"Leaf node {self} has no value.")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if not self.value:
            raise ValueError(f"Leaf node {self} has no value.")
        if not self.tag:
            return self.value
        
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
                
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


        


        
        
        