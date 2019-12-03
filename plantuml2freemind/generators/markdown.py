from typing import Optional, Any

def entry(tree: Any) -> str:
    return convert_tree_into_md(
        root_node_data=tree,
    )


def convert_tree_into_md(root_node_data) -> str:
    level = 0
    result = create_md_node(root_node_data, level)
    result += "\n"
    level += 1
    for branch_name in ['right', 'left']:
        branch = root_node_data[branch_name]
        for node_data in branch:
            result += create_md_node_tree(node_data, level, side=branch_name)

    return result


def create_md_node_tree(node_data, level, side: Optional[str] = None):
    md_node = "\n"
    md_node += create_md_node(node_data, level)
    level += 1
    for child_node_data in node_data['children']:
        md_node += create_md_node_tree(
            node_data=child_node_data,
            level = level
        )
    return md_node


def create_md_node(node_data, level):
    content = node_data['text']
    print(node_data['link'])
    if node_data['link'] is not None:
        content = "[{text}]({link})".format(
            text = node_data['text'],
            link = node_data['link']
        )

    if node_data['style'] == 'bubble':
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

