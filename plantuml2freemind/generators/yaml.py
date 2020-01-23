import yaml

from plantuml2freemind.custom_types import RootNode


def entry(tree: RootNode) -> str:
    return yaml.dump_all(
        documents=[tree.to_dict()],
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
