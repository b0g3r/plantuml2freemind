import xml.etree.ElementTree as ET
from datetime import datetime
from io import StringIO
from typing import Optional

from plantuml2freemind.custom_types import MindmapTreeType

now = str(datetime.utcnow().timestamp())


def entry(tree: MindmapTreeType) -> str:
    return convert_tree_into_mm(
        root_node_data=tree,
    )


def convert_tree_into_mm(root_node_data) -> str:
    xml_map = ET.Element('map')
    xml_map.set('version', '1.0.1')
    root_xml_node = create_xml_node(xml_map, root_node_data, side=None)
    for branch_name in ['left', 'right']:
        branch = root_node_data[branch_name]
        parent = root_xml_node
        for node_data in branch:
            create_xml_node_tree(parent, node_data, side=branch_name)
    xml_tree = ET.ElementTree(xml_map)
    file_obj = StringIO()
    xml_tree.write(file_obj, 'unicode')
    file_obj.write('\n')
    return file_obj.getvalue()


def create_xml_node(parent_xml_node, node_data, side: Optional[str]):
    xml_node = ET.SubElement(parent_xml_node, 'node')
    xml_node.set('TEXT', node_data['text'])
    if node_data['style'] is not None:
        xml_node.set('STYLE', node_data['style'])
    if node_data['link'] is not None:
        xml_node.set('LINK', node_data['link'])
    if node_data['color'] is not None:  
        xml_edge = ET.SubElement(xml_node, 'edge')
        xml_edge.set('COLOR', node_data['color'])

    xml_node.set('CREATED', now)
    xml_node.set('MODIFIED', now)
    if side is not None:
        xml_node.set('POSITION', side)
    return xml_node


def create_xml_node_tree(parent, node_data, side: Optional[str] = None):
    xml_node = create_xml_node(parent, node_data, side)
    for child_node_data in node_data['children']:
        create_xml_node_tree(
            parent=xml_node,
            node_data=child_node_data,
        )
    return xml_node

