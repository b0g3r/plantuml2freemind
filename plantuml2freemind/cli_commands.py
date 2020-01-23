import os.path

from cleo import Command

from plantuml2freemind.generators import GENERATORS
from plantuml2freemind.parsers import PARSERS

SUPPORTED_INPUT_FORMATS = PARSERS.keys()
SUPPORTED_OUTPUT_FORMATS = GENERATORS.keys()


class ConvertCommand(Command):
    """
    Convert from one mindmap file format to another format. Uses YAML tree file as intermediate format.

    convert
        {input-path : Path to source file for converting, e.g. <info>teamlead.puml</info>}
        {output-path : Path to output file for converting, e.g. <info>teamlead.mm</info>}
    """

    def handle(self) -> None:
        input_path = self.argument('input-path')
        output_path = self.argument('output-path')

        if not os.path.isfile(input_path):
            self.line_error(
                'Input path \'{0}\' does not exist'.format(
                    input_path
                ),
                style='error',
            )
            return

        if os.path.isfile(output_path):
            if not self.confirm('Output path \'{0}\' is not empty. Do you want to overwrite it?'.format(output_path), default=True):
                return

        _, input_format = os.path.splitext(input_path)
        if not self.confirm('Input file format is {0}?'.format(input_format), default=True):
            input_format = self.choice(
                'Choose on of supported formats',
                choices=SUPPORTED_INPUT_FORMATS,
            )

        if input_format not in SUPPORTED_INPUT_FORMATS:
            self.line_error(
                '{0} is invalid format for input file. Tool supported formats: {1}'.format(
                    input_format,
                    ', '.join(SUPPORTED_INPUT_FORMATS),
                ),
                style='error',
            )
            return

        _, output_format = os.path.splitext(output_path)
        if not self.confirm('Output file format is {0}?'.format(output_format), default=True):
            output_format = self.choice(
                'Choose on of supported formats',
                choices=SUPPORTED_OUTPUT_FORMATS,
            )
        if output_format not in SUPPORTED_OUTPUT_FORMATS:
            self.line_error(
                '{0} is invalid format for output file. Tool supported formats: {1}'.format(
                    output_format,
                    ', '.join(SUPPORTED_OUTPUT_FORMATS),
                ),
                style='error',
            )
            return

        with open(input_path, 'r') as input_file:
            parser = PARSERS[input_format]
            tree = parser(input_file.read())
        with open(output_path, 'w') as output_file:
            generator = GENERATORS[output_format]
            output_file.write(generator(tree))

        self.line('Successful!', style='info')
