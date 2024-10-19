
type HTMLNode_List = list[HTMLNode]
type HTMLNode_Props = dict[str, str]

from functools import reduce

class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: HTMLNode_List = None, props: HTMLNode_Props = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children.copy() if children != None else None
        self.props = props.copy() if props != None else None
    
    def to_html(self):
        raise NotImplementedError("should be implemented by children")

    def props_to_html(self):
        if self.props == None:
            return ""
        prop_to_str = lambda key: f"{key}={self.props[key]}"
        return reduce(lambda result, key: result + " " + prop_to_str(key), self.props, "")
    
    def __repr__(self) -> str:
        props_str = self.props_to_html()
        children_str = reduce(lambda r, c: r + f"{c}\n", self.children, "------\nchildren:\n") + "------" if self.children != None else "\nno children\n"
        return f"HTML Node : tag={self.tag} value={self.value}\n{children_str}\nprops:{props_str}"