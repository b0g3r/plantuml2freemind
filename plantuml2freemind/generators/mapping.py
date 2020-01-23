from typing import Dict

from plantuml2freemind.custom_types import GeneratorType
from plantuml2freemind.generators import freemind, yaml, markdown

GENERATORS: Dict[str, GeneratorType] = {
    '.mm': freemind.entry,
    '.yaml': yaml.entry,
    '.md': markdown.entry
}