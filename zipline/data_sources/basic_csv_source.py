import datetime
import pytz

from zipline.data_sources.data_source import DataSource


def date_conversion(date_str):
    """
    Convert date strings from TickData (or other source) into epoch values.

    Specify to_utc=False if the input date is already UTC (or is naive).
    """
    dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    dt = dt.replace(tzinfo=pytz.utc)
    return dt


class BasicCSVSource(DataSource):
    """
    A basic CSV source that has the same fields as Yahoo finance.
    """

    def __init__(self, csv_reader):
        self.csv_reader = csv_reader

    @property
    def mapping(self):
        return {
            'sid': (str, 'Symbol'),
            'open': (float, 'Open'),
            'close': (float, 'Close'),
            'high': (float, 'High'),
            'low': (float, 'Low'),
            'volume': (int, 'Volume'),
            'dt': (date_conversion, 'Date')
        }

    @property
    def raw_data(self):
        return self.csv_reader
