# plantuml2freemind


Converts plantuml mindmaps to FreeMind .mm files.

Created especially for [Teamlead Roadmap](https://github.com/tlbootcamp/tlroadmap) project, which stores and
maintains a big community-driven roadmap in a mindmap. It's very convenient to have text plantuml as a source
format and generate other required formats from it.

## Prerequisites

- python >= 3.7 

## Installation

`pip install plantuml2freemind`

## Usage

`plantuml2freemind --help` or `python -m plantuml2freemind --help`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Local development
The project uses poetry as a dependency management tool. For local development convenient way to installing and
running project is using `poetry install`. Please, use [>=1.0.0 version](https://pypi.org/project/poetry/#history) of
poetry even if it is a beta-version.

Poetry automatically creates venv (or uses already activated venv) and install all requirements to it and the project
itself as `editable` . After installing you can run project as a typical python script 
(`python plantuml2freemind/cli.py --help`) or as python's package entry_point (`plantuml2freemind --help`)

TIP: Use `poetry shell` or `poetry run` before running commands: they activate venv. If you want to connect venv to
your IDE, use `poetry env list --full-path`

## License
[MIT](https://choosealicense.com/licenses/mit/)