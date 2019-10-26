import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

now = str(datetime.utcnow().timestamp())


def create_xml_node(parent_xml_node, node_data, side: Optional[str]):
    xml_node = ET.SubElement(parent_xml_node, 'node')
    xml_node.set('TEXT', node_data['text'])
    # xml_node.set('LINK', node_data['link'])
    xml_node.set('CREATED', now)
    xml_node.set('MODIFIED', now)
    if side is not None:
        xml_node.set('POSITION', side)
    return xml_node


def converted_mindmap_tree_into_mm(root_node_data, out_fp):
    xml_map = ET.Element('map')
    xml_map.set('version', '1.0.1')
    root_xml_node = create_xml_node(xml_map, root_node_data, side=None)
    for branch_name in ['left', 'right']:
        branch = root_node_data[branch_name]
        parent = root_xml_node
        for node_data in branch:
            create_xml_node_tree(parent, node_data, side=branch_name)
    tree = ET.ElementTree(xml_map)
    tree.write(out_fp, 'utf-8')
    out_fp.write(b'\n')


def create_xml_node_tree(parent, node_data, side: Optional[str] = None):
    xml_node = create_xml_node(parent, node_data, side)
    for child_node_data in node_data['children']:
        create_xml_node_tree(
            parent=xml_node,
            node_data=child_node_data,
        )
    return xml_node


d = {'children': [],
 'has_box': True,
 'left': [{'children': [{'children': [{'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Умение учиться'},
                                      {'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Рефлексия'},
                                      {'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Выработка привычек'}],
                         'has_box': False,
                         'level': 3,
                         'side': 'left',
                         'text': 'Развитие себя'},
                        {'children': [{'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Эмпатия'},
                                      {'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Эмоциональный интеллект'},
                                      {'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Понимание ценности различий'}],
                         'has_box': False,
                         'level': 3,
                         'side': 'left',
                         'text': 'Отношения'},
                        {'children': [{'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Системное мышление'},
                                      {'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Стратегическое видение'},
                                      {'children': [],
                                       'has_box': False,
                                       'level': 4,
                                       'side': 'left',
                                       'text': 'Принятие решений'}],
                         'has_box': False,
                         'level': 3,
                         'side': 'left',
                         'text': 'Мышление'},
                        {'children': [],
                         'has_box': False,
                         'level': 3,
                         'side': 'left',
                         'text': 'Стили управления'},
                        {'children': [],
                         'has_box': False,
                         'level': 3,
                         'side': 'left',
                         'text': 'Коммуникации'},
                        {'children': [],
                         'has_box': False,
                         'level': 3,
                         'side': 'left',
                         'text': 'Тайм-менеджемент'}],
           'has_box': True,
           'level': 2,
           'side': 'left',
           'text': 'Personal Skills'}],
 'level': 1,
 'right': [],
 'side': None,
 'text': 'Teamlead Roadmap'}