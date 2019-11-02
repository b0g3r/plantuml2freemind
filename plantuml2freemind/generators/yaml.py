import yaml

from plantuml2freemind.custom_types import MindmapTreeType


def entry(tree: MindmapTreeType) -> str:
    # mypy distributed with fixed typeshed version and in mypy 0.740
    # it has misleading stub file for yaml library: https://github.com/python/typeshed/pull/3417
    # TODO: remove `type: ignore` after updating to 0.750 or above
    return yaml.dump_all(  # type: ignore
        documents=[tree],
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )