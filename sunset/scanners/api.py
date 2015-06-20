import abc
import logging

log = logging.getLogger(__name__)


class Scanner(object):
    @abc.abstractmethod
    def match_filetype(self, filetype):
        # subclass must implement logic to determine whether scanner supports a file type
        return False

    @abc.abstractmethod
    def scan(self, stream, parser):
        # subclass must implement extraction of comments from source
        # and pass them to the provided parser (see sunset.parser module).
        raise NotImplementedError()

    @classmethod
    def find_by_filetype(cls, filetype):
        scanners = []

        for scannercls in cls.__subclasses__():
            scanner = scannercls()
            if scanner.match_filetype(filetype):
                scanners.append(scanner)

        return scanners


