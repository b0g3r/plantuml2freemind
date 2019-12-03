from plantuml2freemind.generators import freemind, yaml, markdown

GENERATORS = {
    '.mm': freemind.entry,
    '.yaml': yaml.entry,
    '.md': markdown.entry
}