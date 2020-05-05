from typing import Dict

from plantuml2freemind.custom_types import GeneratorType
from plantuml2freemind.generators import freemind, markdown, plantuml, yaml

GENERATORS: Dict[str, GeneratorType] = {
    ".mm": freemind.entry,
    ".yaml": yaml.entry,
    ".md": markdown.entry,
    ".puml": plantuml.entry,
}
