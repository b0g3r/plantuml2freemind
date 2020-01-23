import re
from typing import List

from plantuml2freemind.custom_types import ParserNode, RootNode


def entry(file_content: str) -> RootNode:
    nodes = list(extract_nodes(file_content))
    tree = combine_tree(nodes)
    return tree


def extract_nodes(file_content: str) -> List[ParserNode]:
    file_content = file_content.strip()
    if not file_content.startswith('@startmindmap') or not file_content.endswith('@endmindmap'):
        raise TypeError('Plantuml mindmaps should started with @startmindmap and ends with @endmindmap')
    # TODO: skip caption/title/header
    nodes_lines = [line.rstrip() for line in file_content.split('\n')[1:-1] if line]
    # default side in puml mindmaps is right
    side = 'right'
    nodes = []
    for node_line in nodes_lines:
        if node_line == 'left side':
            side = 'left'
            continue
        nodes.append(parse_line(node_line, side))
    return nodes


def parse_line(line: str, side: str) -> ParserNode:
    """
    Return structured data about line from .puml mindmap file.
    """
    # TODO: parse not only org mode
    return parse_line_org_mode(line, side)


def parse_line_org_mode(line: str, side: str) -> ParserNode:
    """
    Parse OrgMode format.

    For example: `*** KDE Neon` is text "KDE Neon" on third nesting level.
    """
    line = line.strip()
    left_part, right_part = line.split(' ', maxsplit=1)
    nesting_level = left_part.count('*')
    style = 'fork' if left_part.endswith('_') else 'bubble'

    match = re.search('\[(#[a-f0-9]{6})\]', left_part)
    color = match.group(1) if match else None

    match = re.search('\[\[([a-zA-Zа-яА-Я:\/.-]*) ?([\W\w]*)?\]\]', right_part)
    link = match.group(1) if match else None
    text = match.group(2) if match else right_part.strip()

    node_data = ParserNode(
        text=text,
        link=link,
        level=nesting_level,
        color=color,
        style=style,
        side=side,
    )

    return node_data


def combine_tree(nodes: List[ParserNode]) -> RootNode:
    first, *children = nodes
    if not first.is_root:
        raise ValueError('The first node in the list is not a valid root node')
    root = first.to_root()
    for child in children:
        root.add_node(child)
    return root
