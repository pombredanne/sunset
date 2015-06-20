import mock
import os
import sunset.tool

from datetime import date, timedelta

from sunset.parser import Marker


class TestScanTool(object):
    def test_scan_files_single_file(self):
        filename = os.path.join(os.curdir, 'tests', 'scan_test', 'file_a.py')

        scantool = sunset.tool.ScanTool(sunset.tool.ScanLog())
        scantool.targets = [filename]
        files = list(scantool.scan_files())
        assert len(files) == 1
        assert files[0] == os.path.abspath(filename)

    def test_scan_files_directory(self):
        dirname = os.path.join(os.curdir, 'tests', 'scan_test', 'inner')
        filename = os.path.abspath(os.path.join(os.curdir, 'tests', 'scan_test', 'inner', 'file_b.py'))

        scantool = sunset.tool.ScanTool(sunset.tool.ScanLog())
        scantool.targets = [dirname]
        files = list(scantool.scan_files())
        assert len(files) == 1
        assert files[0] == filename

    def test_scan_files_recursive(self):
        dirname = os.path.join(os.curdir, 'tests', 'scan_test')
        filenames = map(os.path.abspath,
                    map(lambda files: os.path.join(os.curdir, 'tests', 'scan_test', *files),
                        [('file_a.py',),
                         ('inner', 'file_b.py')]))

        scantool = sunset.tool.ScanTool(sunset.tool.ScanLog())
        scantool.targets = [dirname]
        scantool.recursive = True

        files = list(scantool.scan_files())
        assert len(files) == 2
        assert sorted(files) == sorted(filenames)

    def test_check_markers(self):
        mock_scan_log = mock.Mock(spec=sunset.tool.ScanLog)()
        scantool = sunset.tool.ScanTool(mock_scan_log)

        marker = Marker(1)
        marker.expires = date.today() + timedelta(days=1)
        scantool.check_markers('', [marker])

        assert mock_scan_log.warn.called
        mock_scan_log.reset_mock()

        marker.expires = date.today() - timedelta(days=1)
        scantool.check_markers('', [marker])
        assert mock_scan_log.alert.called

    def test_start_scan(self):
        stored_markers = []

        def mocked_check_markers(self, filename, markers):
            stored_markers.append(markers)

        original = sunset.tool.ScanTool.check_markers

        try:
            sunset.tool.ScanTool.check_markers = mocked_check_markers

            scantool = sunset.tool.ScanTool(sunset.tool.ScanLog())
            scantool.targets = [os.path.join(os.curdir, 'tests', 'scan_test')]
            scantool.recursive = True
            scantool.start_scan()
            assert len(stored_markers) == 2
            assert sum(map(len, stored_markers)) == 4
        finally:
            sunset.tool.ScanTool.check_markers = original

