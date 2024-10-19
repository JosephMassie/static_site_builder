
type HTMLNode_List = list[HTMLNode]
type HTMLNode_Props = dict[str, str]

from functools import reduce

def create_tag(tag: str, props: str = "", is_close: bool = False) -> str:
    return f"<{"/" if is_close == True else ""}{tag}{props}>"

class HTMLNode():
    def __init__(self, *, tag: str = None, value: str = None, children: HTMLNode_List = None, props: HTMLNode_Props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children.copy() if children != None else None
        self.props = props.copy() if props != None else None
    
    def to_html(self):
        raise NotImplementedError("should be implemented by children")

    def props_to_html(self):
        if self.props == None:
            return ""
        prop_to_str = lambda key: f"{key}=\"{self.props[key]}\""
        return reduce(lambda result, key: result + " " + prop_to_str(key), self.props, "")
    
    def __repr__(self) -> str:
        props_str = self.props_to_html()
        children_str = reduce(lambda r, c: r + f"{c}\n", self.children, "------\nchildren:\n") + "------" if self.children != None else "\nno children\n"
        return f"HTML Node : tag={self.tag} value={self.value}\n{children_str}\nprops:{props_str}"

class LeafNode(HTMLNode):
    def __init__(self, *, tag: str = None, value: str, props: HTMLNode_Props = None) -> None:
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNodes must have a value")
        
        string = self.value
        if self.tag != None:
            open = create_tag(self.tag, self.props_to_html())
            close = create_tag(self.tag, is_close=True)
            string = open + string + close
        return string

class ParentNode(HTMLNode):
    def __init__(self, *, tag: str, children: HTMLNode_List, props: HTMLNode_Props = None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None or len(self.children) == 0:
            raise ValueError("ParentNode must contain children")

        string = "<" + self.tag + ">"
        string = reduce(lambda r, c: r + c.to_html(), self.children, string)
        string += "</" + self.tag + ">"
        return string