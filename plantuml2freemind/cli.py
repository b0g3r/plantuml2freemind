from plantuml2freemind import __version__

from cleo import Application

from plantuml2freemind.cli_commands import ConvertCommand

application = Application(
    name='plantuml2freemind',
    version=__version__,
)
application.add(ConvertCommand())


def main():
    application.run()


if __name__ == '__main__':
    main()
