import csv
import datetime
import pytz
from StringIO import StringIO

from unittest import TestCase

from zipline.data_sources.basic_csv_source import BasicCSVSource

BASIC_CSV_VALUES = """
Symbol,Open,Close,High,Low,Volume,Date
IBM,100.0,120.0,125.0,90.0,1234,2008-07-06
""".strip()


class TestBasicCSVSource(TestCase):

    def test_basic_load(self):

        raw_source = csv.DictReader(StringIO(BASIC_CSV_VALUES))

        source = BasicCSVSource(raw_source)

        output = list(source)

        self.assertEquals(1, len(output))

        row = output.pop()

        self.assertEquals(row['sid'], 'IBM')
        self.assertEquals(row['open'], 100.0)
        self.assertEquals(row['close'], 120.0)
        self.assertEquals(row['high'], 125.0)
        self.assertEquals(row['low'], 90.0)
        self.assertEquals(row['dt'],
                          datetime.datetime(2008, 07, 06, tzinfo=pytz.utc))
