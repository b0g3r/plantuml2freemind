from typing import List, Dict, Any

import yaml


def entry(input_file_name: str, output_file_name: str) -> None:
    tree = parse_file(input_file_name)
    with open(output_file_name, 'w') as output_file:
        # mypy distributed with fixed typeshed version and in mypy 0.740
        # it has misleading stub file for yaml library: https://github.com/python/typeshed/pull/3417
        # TODO: remove `type: ignore` after updating to 0.750 or above
        yaml.dump_all(  # type: ignore
            documents=[tree],
            stream=output_file,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )


def parse_file(file_name: str) -> Dict[str, Any]:
    with open(file_name, 'r') as puml_file:
        file_content = puml_file.read()
    nodes = list(extract_nodes(file_content))
    tree = combine_tree(nodes)
    return tree


def extract_nodes(file_content: str) -> List[Dict[str, Any]]:
    file_content = file_content.strip()
    if not file_content.startswith('@startmindmap') or not file_content.endswith('@endmindmap'):
        raise TypeError('Plantuml mindmaps should started with @startmindmap and ends with @endmindmap')
    # TODO: skip caption/title/header
    nodes_lines = [line.rstrip() for line in file_content.split('\n')[1:-1] if line]
    # default side in puml mindmaps
    side = 'right'
    nodes = []
    for node_line in nodes_lines:
        if node_line == 'left side':
            side = 'left'
            continue
        nodes.append(parse_line(node_line, side))
    return nodes


def parse_line(line: str, side: str) -> Dict[str, Any]:
    """
    Return structured data about line from .puml mindmap file.
    """
    # TODO: parse not only org mode
    return parse_line_org_mode(line, side)


def parse_line_org_mode(line: str, side: str) -> Dict[str, Any]:
    """
    Parse OrgMode format.

    For example: `*** KDE Neon` is text "KDE Neon" on third nesting level.
    """
    line = line.strip()
    left_part, right_part = line.split(' ', maxsplit=1)
    nesting_level = left_part.count('*')
    style = 'fork' if left_part.endswith('_') else 'bubble'
    node_data: Dict[str, Any] = {
        'text': right_part.strip(),
        'link': None,
        'level': nesting_level,
        'side': side,
        'style': style,
        'children': [],
    }
    return node_data


def combine_tree(nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
    root = nodes[0]
    root['left'] = []
    root['right'] = []
    root.pop('children')
    for node in nodes[1:]:
        add_node(root, node)
    return root


def add_node(root: Dict[str, Any], node: Dict[str, Any]) -> None:
    level = node['level']
    if level < 2:
        return
    side = node['side']
    children = root[side]
    for _ in range(level - 2):
        children = children[-1]['children']
    node.pop('level')
    node.pop('side')
    children.append(node)
