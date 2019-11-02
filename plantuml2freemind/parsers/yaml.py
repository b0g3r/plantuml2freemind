import yaml

from plantuml2freemind.custom_types import MindmapTreeType


def entry(file_content: str) -> MindmapTreeType:
    return yaml.safe_load(file_content)
