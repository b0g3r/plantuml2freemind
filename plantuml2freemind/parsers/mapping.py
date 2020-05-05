from typing import Dict

from plantuml2freemind.custom_types import ParserType
from plantuml2freemind.parsers import plantuml, yaml

PARSERS: Dict[str, ParserType] = {
    ".puml": plantuml.entry,
    ".yaml": yaml.entry,
    ".json": yaml.entry,
}
