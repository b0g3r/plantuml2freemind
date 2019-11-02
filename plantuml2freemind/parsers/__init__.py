"""
This module contains parsers: functions which accept mindmap file at the input
and generate YAML file with tree structure and extracted data.

For example: plantuml (.puml) to yaml
"""
from plantuml2freemind.parsers.mapping import PARSERS

__all__ = [
    'PARSERS',
]