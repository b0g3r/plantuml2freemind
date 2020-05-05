from typing import Union

from plantuml2freemind.custom_types import ChildNode, RootNode

AnyNode = Union[RootNode, ChildNode]


def entry(tree: RootNode) -> str:
    return convert_tree_into_puml(root=tree)


def concat_pumls(lhs: str, rhs: str):
    return f"{lhs}\n{rhs}"


def generate_markdown(node: AnyNode) -> str:
    return f"[[{node.link} {node.text}]]"


def generate_puml_node(node: AnyNode, level: int) -> str:
    prefix = "*" * level
    text = node.text if not node.link else generate_markdown(node)
    style = "_" if node.style == "fork" else ""
    return f"{prefix}{style} {text}"


def generate_branch(subtree: ChildNode, level) -> str:
    node = generate_puml_node(subtree, level)
    for child in subtree.children:
        node = concat_pumls(node, generate_branch(child, level + 1))
    return node


def convert_tree_into_puml(root: RootNode) -> str:
    """Generate PlantUML mindmap from tree."""
    puml = generate_puml_node(root, 1)

    if root.right:
        puml = concat_pumls(puml, generate_branch(root.right, 2))
        puml += f"\nleft side"

    if root.left:
        puml = concat_pumls(puml, generate_branch(root.left, 2))

    return "\n".join(("@startmindmap", puml, "@endmindmap"))
