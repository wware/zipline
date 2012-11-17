from abc import (
    ABCMeta,
    abstractproperty
)

from zipline.protocol import DATASOURCE_TYPE
from zipline.utils.protocol_utils import ndict


class DataSource(object):

    __metaclass__ = ABCMeta

    @property
    def event_type(self):
        return DATASOURCE_TYPE.TRADE

    @property
    def mapping(self):
        """
        Mappings of the form:
        target_key: (mapping_function, source_key)
        """
        return {}

    @abstractproperty
    def raw_data(self):
        """
        An iterator that yields the raw datasource,
        in chronological order of data, one event at a time.
        """
        NotImplemented

    @property
    def source_id(self):
        return self.__class__.__name__

    def apply_mapping(self, raw_row):
        """
        Override this to hand craft conversion of row.
        """
        row = {target: mapping_func(raw_row[source_key])
               for target, (mapping_func, source_key)
               in self.mapping.items()}
        row.update({'source_id': self.source_id})
        row.update({'type': self.event_type})
        return row

    def __iter__(self):
        for row in self.raw_data:
            yield ndict(self.apply_mapping(row))
