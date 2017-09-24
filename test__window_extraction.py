import pytest
import pandas
from window_extraction import *


@pytest.fixture(scope='module')
def get_swing_data():
    batting_file_path = 'latestSwing.csv'
    batting_data = pandas.read_csv(batting_file_path)
    return batting_data


test_series = pandas.Series([0, 1, 1, 0, 1, 5, 1, 0, 1, 2, 0, 2, 2, 0])
def input_args(data=test_series, indexBegin=3, indexEnd=9, threshold=0.5, winLength=2):
    return {'data': data, 'indexBegin': indexBegin, 'indexEnd': indexEnd,
            'threshold': threshold, 'winLength': winLength}


@pytest.mark.parametrize('test_name,input_dict,expected', [
    ('basic test', input_args(), 4),
    ('earlier start', input_args(indexBegin=0), 1),
    ('one data point', input_args(indexBegin=0, indexEnd=0), None),
    ('higher threshold', input_args(threshold=1.5, indexEnd=12), 11),
    ('single point at indexbegin', input_args(winLength=1, indexBegin=2), 2),
    ('single point after indexbegin', input_args(winLength=1, indexBegin=0), 1),
    ('larger window', input_args(winLength=3, indexBegin=0), 4),
    ('2 points w window of 3', input_args(winLength=3, indexBegin=0, indexEnd=1, threshold=-1), None),
    ('at threshold float', input_args(threshold=0.99999), 4),
    ('at threshold int', input_args(indexEnd=12, threshold=1), 11),
    ('at threshold float', input_args(indexEnd=12, threshold=1.0), 11),
])
def test_searchContinuityAboveValue(test_name, input_dict, expected):
    print(test_name)
    result = searchContinuityAboveValue(**input_dict)
    assert result == expected


def input_args(data=test_series, indexBegin=3, indexEnd=9, thresholdLo=0.5, thresholdHi=4.5, winLength=2):
    return {'data': data, 'indexBegin': indexBegin, 'indexEnd': indexEnd,
            'thresholdLo': thresholdLo, 'thresholdHi': thresholdHi, 'winLength': winLength}


@pytest.mark.parametrize('test_name,input_dict,expected', [
    ('basic test', input_args(), [(8, 9)]),
    ('higher threshold', input_args(thresholdHi=5.1), [(4, 6), (8, 9)]),
    ('at higher threshold', input_args(thresholdHi=5.0), [(8, 9)]),
    ('small window', input_args(winLength=1), [(4, 4), (6, 6), (8, 9)]),
    ('too large window', input_args(winLength=4), []),
    ('too large window', input_args(winLength=3), []),
    ('further end index', input_args(indexEnd=12), [(8, 9), (11, 12)]),
    ('lower threshold over upper', input_args(thresholdLo=5), []),
    ('ending on part of window', input_args(indexEnd=11), [(8, 9)]),
    ('starting on partial window', input_args(indexBegin=2), [(8, 9)]),
])
def test_searchMultiContinuityWithinRange(test_name, input_dict, expected):
    print(test_name)
    result = searchMultiContinuityWithinRange(**input_dict)
    assert result == expected


if __name__ == '__main__':
    pytest.main()
