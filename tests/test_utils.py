#
# Copyright 2012 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest2 import TestCase
from zipline.utils.factory import load_from_yahoo
import pandas as pd
import pytz
import numpy as np
from datetime import datetime

from zipline.utils.date_utils import get_quarter, dates_of_quarter


class TestFactory(TestCase):
    def test_load_from_yahoo(self):
        stocks = ['AAPL', 'GE']
        start = pd.datetime(1993, 1, 1, 0, 0, 0, 0, pytz.utc)
        end = pd.datetime(2002, 1, 1, 0, 0, 0, 0, pytz.utc)
        data = load_from_yahoo(stocks=stocks, start=start, end=end)

        assert data.index[0] == pd.Timestamp('1993-01-04 00:00:00+0000')
        assert data.index[-1] == pd.Timestamp('2001-12-31 00:00:00+0000')
        for stock in stocks:
            assert stock in data.columns

        np.testing.assert_raises(
            AssertionError, load_from_yahoo, stocks=stocks,
            start=end, end=start
        )


class TestDateUtils(TestCase):

    def test_quarter(self):
        # the following list of tuples are dates, quarter
        # numbers, quarter start, quarter end. They were
        # calculated by hand.
        answer_key = [
                (datetime(1970,1,2,tzinfo=pytz.utc),
                    7880,
                    datetime(1970,1,1,0,0,tzinfo=pytz.utc),
                    datetime(1970,3,31,23,59,tzinfo=pytz.utc)),
                (datetime(2002,5,18,tzinfo=pytz.utc),
                    8009,
                    datetime(2002,4,1,0,0,tzinfo=pytz.utc),
                    datetime(2002,6,30,23,59,tzinfo=pytz.utc)),
                (datetime(2011,8,19,tzinfo=pytz.utc),
                    8046,
                    datetime(2011,7,1,0,0,tzinfo=pytz.utc),
                    datetime(2011,9,30,23,59,tzinfo=pytz.utc)),
                (datetime(2006,10,2,tzinfo=pytz.utc),
                    8027,
                    datetime(2006,10,1,0,0,tzinfo=pytz.utc),
                    datetime(2006,12,31,23,59,tzinfo=pytz.utc)),
                ]

        for pair in answer_key:
            q = get_quarter(pair[0])
            self.assertEqual(pair[1], q)
            start, end = dates_of_quarter(q)
            self.assertEqual(pair[2], start)
            self.assertEqual(pair[3], end)
