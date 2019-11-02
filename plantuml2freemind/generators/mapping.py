from plantuml2freemind.generators import freemind, yaml

GENERATORS = {
    '.mm': freemind.entry,
    '.yaml': yaml.entry,
}