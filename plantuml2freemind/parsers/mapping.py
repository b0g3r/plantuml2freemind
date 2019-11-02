from plantuml2freemind.parsers import plantuml, yaml

PARSERS = {
    '.puml': plantuml.entry,
    '.yaml': yaml.entry,
}