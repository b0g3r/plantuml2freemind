"""
This module contains generators: functions which accept YAML mindmap at the input
and generate output file in mindmap format.

For example: yaml to freemind (.mm), yaml to plantuml (.puml).
"""
from plantuml2freemind.generators.mapping import GENERATORS

__all__ = [
    'GENERATORS'
]