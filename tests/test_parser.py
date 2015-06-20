from datetime import date
from sunset.parser import Parser, Marker


class TestMarker(object):
    def test_str_for_single_line(self):
        marker = Marker(10)
        marker.expires = date(2014, 12, 25)
        assert str(marker) == 'Marker(line=10, expires=2014-12-25)'
        assert repr(marker) == str(marker)

    def test_str_for_multiline(self):
        marker = Marker(10)
        marker.expires = date(2014, 12, 25)
        marker.line_end = 15
        assert str(marker) == 'Marker(line=10-15, expires=2014-12-25)'
        assert repr(marker) == str(marker)


class TestParser(object):
    def test_parse_begin_matches_valid_date_format(self):
        parser = Parser()
        parser.parse_begin(1, '# >>SUNSET 2014-12-01<<')
        assert len(parser.markers) == 1
        assert parser.markers[0].expires == date(2014, 12, 1)

    def test_parse_begin_does_not_match_invalid_year(self):
        parser = Parser()
        parser.parse_begin(1, '# >>SUNSET 114-12-01<<')
        assert len(parser.markers) == 0

    def test_parse_begin_does_not_match_invalid_month(self):
        parser = Parser()
        parser.parse_begin(1, '# >>SUNSET 2001-0-01<<')
        assert len(parser.markers) == 0
        parser.parse_begin(1, '# >>SUNSET 2001-00-01<<')
        assert len(parser.markers) == 0
        parser.parse_begin(1, '# >>SUNSET 2001-13-01<<')
        assert len(parser.markers) == 0

    def test_parse_begin_does_not_match_invalid_day(self):
        parser = Parser()
        parser.parse_begin(1, '# >>SUNSET 2001-01-0<<')
        assert len(parser.markers) == 0
        parser.parse_begin(1, '# >>SUNSET 2001-01-00<<')
        assert len(parser.markers) == 0
        parser.parse_begin(1, '# >>SUNSET 2001-01-32<<')
        assert len(parser.markers) == 0
        parser.parse_begin(1, '# >>SUNSET 2001-01-40<<')
        assert len(parser.markers) == 0

    def test_parse_end_matches_open_marker(self):
        parser = Parser()
        parser.parse_begin(1, '# >>SUNSET 2014-12-01')
        assert len(parser.markers) == 0
        parser.parse_end(2, '# <<SUNSET')
        assert len(parser.markers) == 1
        assert parser.markers[0].expires == date(2014, 12, 1)

    def test_parse_matches_single_line(self):
        parser = Parser()
        parser.parse(1, '# >>SUNSET 2014-12-01<<')
        assert len(parser.markers) == 1
        assert parser.markers[0].expires == date(2014, 12, 1)

    def test_parse_matches_multiline(self):
        parser = Parser()
        parser.parse(1, '# >>SUNSET 2014-12-01<<')
        parser.parse(2, '# <<SUNSET')
        assert len(parser.markers) == 1
        assert parser.markers[0].expires == date(2014, 12, 1)
