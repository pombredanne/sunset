from StringIO import StringIO

from sunset.scanners.api import Scanner
from sunset.scanners.python import PythonScanner


class MockScanner(Scanner):
    def match_filetype(self, filetype):
        return filetype == 'mock'

    def scan(self, stream, parser):
        pass


class TestScannerApi(object):
    def test_find_by_filetype_returns_empty_list_when_no_match(self):
        assert Scanner.find_by_filetype('does_not_exist') == []

    def test_find_by_filetype_returns_scanner_in_list_on_match(self):
        assert len(Scanner.find_by_filetype('mock')) == 1
        assert isinstance(Scanner.find_by_filetype('mock')[0], MockScanner)


class TestPythonScanner(object):
    def test_match_filetype_matches_python_extensions(self):
        assert PythonScanner().match_filetype('py') is True

    def test_scan_matches_comments(self):
        class MockParser(object):
            def __init__(self):
                self.received = []

            def parse(self, lineno, comment):
                self.received.append([lineno, comment])

        stream = StringIO('# some comment here\nnot_a_comment()').readline
        parser = MockParser()

        PythonScanner().scan(stream, parser)

        assert len(parser.received) == 1
        assert parser.received[0][1] == '# some comment here'

