import yaml

from plantuml2freemind.custom_types import RootNode


def entry(file_content: str) -> RootNode:
    return RootNode.from_dict(yaml.safe_load(file_content))
