import tokenize

from .api import Scanner


class PythonScanner(Scanner):
    def match_filetype(self, filetype):
        return filetype.lower() == 'py'

    def scan(self, stream, parser):
        for toktype, token, start, _, _ in tokenize.generate_tokens(stream):
            if toktype != tokenize.COMMENT:
                continue

            parser.parse(start[0], token)
