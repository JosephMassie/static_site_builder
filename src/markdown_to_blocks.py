import re
from functools import reduce
from htmlnode import *
from textnode import *

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = map(lambda b: b.strip(), blocks)
    blocks = list(filter(lambda b: b != "", blocks))
    return blocks

def block_to_type(block: str):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    lines = block.split("\n")
    check_every_line = lambda lines, char: reduce(lambda r, l: r and l.startswith(char), lines, True)
    if check_every_line(lines, ">"):
        return "quote"

    if check_every_line(lines, "* ") or check_every_line(lines, "- "):
        return "unordered list"
    
    is_ordered_list = True
    for i in range(len(lines)):
        start = ". " + "".join([" "] * i)
        is_ordered_list = is_ordered_list and lines[i].startswith(start)
    if is_ordered_list:
        return "ordered list"
    
    return "paragraph"

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    get_children = lambda string: list(map(text_node_to_html_node, text_to_textnodes(string)))

    main_child_nodes = []
    for block in blocks:
        block_type = block_to_type(block)
        match block_type:
            case "quote":
                lines = block.splitlines()
                lines = list(map(lambda l: l.lstrip(">"), lines))
                content = "\n".join(lines)
                children = get_children(content)
                quote = ParentNode(tag="quote", children=children)
                main_child_nodes.append(quote)
                pass
            case "ordered list":
                lines = block.splitlines()
                uo_children = []
                for i in range(len(lines)):
                    line = lines[i]
                    rep = ". " + "".join([" "] * i)
                    content = line.replace(rep, "")
                    children = get_children(content)
                    li_item = ParentNode(tag="li", children=children)
                    uo_children.append(li_item)
                uo_list = ParentNode(tag="ol", children=uo_children)
                main_child_nodes.append(uo_list)
                pass
            case "unordered list":
                lines = block.splitlines()
                uo_children = []
                for line in lines:
                    content = line.replace("* ", "").replace("- ", "")
                    children = get_children(content)
                    li_item = ParentNode(tag="li", children=children)
                    uo_children.append(li_item)
                uo_list = ParentNode(tag="ul", children=uo_children)
                main_child_nodes.append(uo_list)
                pass
            case "code":
                content = block.strip("```")
                children = get_children(content)
                code = ParentNode(tag="code", children=children)
                main_child_nodes.append(code)
                pass
            case "heading":
                leading_str = re.findall(r"^(#+) .*", block, re.RegexFlag.MULTILINE)[0]
                heading_type = leading_str.count("#")
                if heading_type > 6:
                    heading_type = 6
                content = block.lstrip("# ")
                children = get_children(content)
                header = ParentNode(tag=f"h{heading_type}", children=children)
                main_child_nodes.append(header)
                pass
            case "paragraph":
                children = get_children(block)
                para = ParentNode(tag="p", children=children)
                main_child_nodes.append(para)
                pass
            case _:
                raise Exception("invalid block type")
    return ParentNode(tag="div", children=main_child_nodes)

def extract_title(markdown: str) -> str:
    match = re.search(r"^# (.*?)$", markdown, re.RegexFlag.MULTILINE)
    if match != None:
        return match.group(1)
    return ""
