import xml.etree.ElementTree as ET
from datetime import datetime
from io import StringIO
from typing import Optional, Union

from plantuml2freemind.custom_types import RootNode, ChildNode

now = str(datetime.utcnow().timestamp())


def entry(tree: RootNode) -> str:
    return convert_tree_into_mm(
        root_node_data=tree,
    )


def convert_tree_into_mm(root_node_data: RootNode) -> str:
    xml_map = ET.Element('map')
    xml_map.set('version', '1.0.1')
    root_xml_node = create_xml_node(xml_map, root_node_data, side=None)
    process_branch(root_xml_node, root_node_data.left, 'left')
    process_branch(root_xml_node, root_node_data.right, 'right')
    xml_tree = ET.ElementTree(xml_map)
    file_obj = StringIO()
    xml_tree.write(file_obj, 'unicode')
    file_obj.write('\n')
    return file_obj.getvalue()


def process_branch(parent: ET.Element, branch: Optional[ChildNode], side: str) -> None:
    if branch is None:
        return
    for node_data in branch.children:
        create_xml_node_tree(parent, node_data, side)


def create_xml_node(parent_xml_node, node: Union[RootNode, ChildNode], side: Optional[str] = None) -> ET.Element:
    xml_node = ET.SubElement(parent_xml_node, 'node')
    xml_node.set('TEXT', node.text)
    if node.style is not None:
        xml_node.set('STYLE', node.style)
    if node.link is not None:
        xml_node.set('LINK', node.link)
    if node.color is not None:
        xml_edge = ET.SubElement(xml_node, 'edge')
        xml_edge.set('COLOR', node.color)

    if side is not None:
        xml_node.set('POSITION', side)
    return xml_node


def create_xml_node_tree(parent: ET.Element, node_data: ChildNode, side: Optional[str] = None) -> ET.Element:
    xml_node = create_xml_node(parent, node_data, side)
    for child_node_data in node_data.children:
        create_xml_node_tree(
            parent=xml_node,
            node_data=child_node_data,
        )
    return xml_node
