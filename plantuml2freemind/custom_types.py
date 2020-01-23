from typing import Any, Container, Dict, List, Optional, NewType

from attr import asdict, attrib, attrs
from attr.validators import in_, instance_of, optional
from typing_extensions import Protocol

LEFT_SIDE = 'left'
RIGHT_SIDE = 'right'
VALID_SIDES = frozenset([LEFT_SIDE, RIGHT_SIDE])


def exclude_keys(d: Dict[str, Any], excluded: Container[str]) -> Dict[str, Any]:
    """
    Helper function for building attr instance from dict without redundant keys.
    """
    return {key: value for key, value in d.items() if key not in excluded}


@attrs
class MindmapTreeNode(object):
    """
    Base structure class for Mindmap (diagram format) node.

    Mindmap diagram can be described as tree (one root node) with two branches where each node in branch can
    have any amount of children. It class uses as generic parent for root and child node.

    More info about mindmaps as format: https://en.wikipedia.org/wiki/Mind_map
    """

    text: str = attrib(validator=instance_of(str))
    link: Optional[str] = attrib()
    style: Optional[str] = attrib()
    color: Optional[str] = attrib()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@attrs(kw_only=True, slots=True)
class ChildNode(MindmapTreeNode):
    """
    Every child node can have any amount of children.
    """
    children: List['ChildNode'] = attrib(
        factory=list,
    )

    def get_last_child(self) -> 'ChildNode':
        if not self.children:
            raise ValueError('Current node has no children')
        return self.children[-1]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Optional['ChildNode']:
        if not d:
            return None
        node = cls(**exclude_keys(d, ['children']))
        children = []
        for child_dict in d.get('children', []):
            child = cls.from_dict(child_dict)
            if child is not None:
                children.append(child)
        node.children = children
        return node


@attrs(kw_only=True, slots=True)
class RootNode(MindmapTreeNode):
    """
    Mindmap has only one root node with two optional branches, left and right.
    """
    right: Optional[ChildNode] = attrib(default=None, validator=optional(instance_of(ChildNode)))
    left: Optional[ChildNode] = attrib(default=None, validator=optional(instance_of(ChildNode)))

    def get_side(self, side: Optional[str]) -> Optional[ChildNode]:
        if side == LEFT_SIDE:
            return self.left
        if side == RIGHT_SIDE:
            return self.right
        raise ValueError('{side} is not a valid value for side'.format(side=side))

    def add_node(self, node: 'ParserNode'):
        if node.level == 1:
            raise ValueError('Trying to add a root node')
        if node.level == 2:
            if node.side == LEFT_SIDE:
                self.left = node.to_child()
            elif node.side == RIGHT_SIDE:
                self.right = node.to_child()
            return

        child = self.get_side(node.side)
        if child is None:
            raise ValueError('{side} child is None'.format(side=node.side))
        for _ in range(node.level - 3):
            child = child.get_last_child()

        child.children.append(node.to_child())

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'RootNode':
        root = cls(**exclude_keys(d, VALID_SIDES))
        left = d.get('left', {})
        right = d.get('right', {})
        root.left = ChildNode.from_dict(left)
        root.right = ChildNode.from_dict(right)
        return root


@attrs(kw_only=True, slots=True, frozen=True)
class ParserNode(MindmapTreeNode):
    """
    When we parse mindmap files we extract nodes as flat list and should also store some meta data.
    """
    level: int = attrib(validator=instance_of(int))
    side: Optional[str] = attrib(validator=optional(in_(VALID_SIDES)))

    @level.validator
    def is_positive(self, attribute, value):
        if value < 1:
            raise ValueError('level must be a positive integer greater than 1')

    @property
    def is_root(self) -> bool:
        return self.level == 1

    def to_node_dict(self):
        return asdict(self, filter=lambda attr, value: attr.name not in ['level', 'side'])

    def to_root(self) -> RootNode:
        return RootNode(**self.to_node_dict())

    def to_child(self) -> ChildNode:
        return ChildNode(**self.to_node_dict())


class GeneratorType(Protocol):
    def __call__(self, tree: RootNode) -> str:
        ...


class ParserType(Protocol):
    def __call__(self, file_content: str) -> RootNode:
        ...
