from typing import Optional, Any
from plantuml2freemind.custom_types import RootNode

def entry(tree: RootNode) -> str:
    return convert_tree_into_md(
        root_node=tree,
    )


def convert_tree_into_md(root_node) -> str:
    level = 0
    result = create_md_node(root_node, level)
    result += "\n"
    level += 1

    result += create_md_node_tree(root_node.right, level, side="right")
    result += create_md_node_tree(root_node.left, level, side="right")

    return result


def create_md_node_tree(node_data, level, side: Optional[str] = None):
    md_node = "\n"
    md_node += create_md_node(node_data, level)
    level += 1
    for child_node_data in node_data.children:
        md_node += create_md_node_tree(
            node_data=child_node_data,
            level = level
        )
    return md_node


def create_md_node(node, level):
    content = node.text
    if node.link is not None:
        content = "[{text}]({link})".format(
            text = node.text,
            link = node.link
        )
    if node.style == 'bubble':
        content = "# {}".format(content)
        for i in range(0, level):
            content = "#" + content
    else:
        if level > 2:
            content = "- {}".format(content)
            for i in range(0, level - 3):
                content = "    " + content
        else:
            content = "# {}".format(content)
            for i in range(0, level):
                content = "#" + content
        
    return content