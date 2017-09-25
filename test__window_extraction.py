import pytest
import pandas
from simple_window_extraction import *


@pytest.fixture(scope='module')
def get_swing_data():
    batting_file_path = 'latestSwing.csv'
    batting_data = pandas.read_csv(batting_file_path)
    return batting_data


test_series = pandas.Series([0, 1, 1, 0, 1, 5, 1, 0, 1, 2, 0, 2, 2, 0])
neg_test_series = test_series * -1


def input_args_1t(data=test_series, indexBegin=3, indexEnd=9, threshold=0.5, winLength=2):
    return {'data': data, 'indexBegin': indexBegin, 'indexEnd': indexEnd,
            'threshold': threshold, 'winLength': winLength}


@pytest.mark.parametrize('test_name,input_dict,expected', [
    ('basic test', input_args_1t(), 4),
    ('earlier start', input_args_1t(indexBegin=0), 1),
    ('one data point', input_args_1t(indexBegin=0, indexEnd=0), None),
    ('higher threshold', input_args_1t(threshold=1.5, indexEnd=12), 11),
    ('single point at indexbegin', input_args_1t(winLength=1, indexBegin=2), 2),
    ('single point after indexbegin', input_args_1t(winLength=1, indexBegin=0), 1),
    ('larger window', input_args_1t(winLength=3, indexBegin=0), 4),
    ('2 points w window of 3', input_args_1t(winLength=3, indexBegin=0, indexEnd=1, threshold=-1), None),
    ('at threshold float', input_args_1t(threshold=0.99999), 4),
    ('at threshold int', input_args_1t(indexEnd=12, threshold=1), 11),
    ('at threshold float', input_args_1t(indexEnd=12, threshold=1.0), 11),
])
def test_searchContinuityAboveValue(test_name, input_dict, expected):
    print(test_name)
    result = searchContinuityAboveValue(**input_dict)
    assert result == expected


def input_args_2t_rev(data=test_series, indexBegin=9, indexEnd=3,
                      thresholdLo=0.5, thresholdHi=4.5, winLength=2):
    return {'data': data, 'indexBegin': indexBegin, 'indexEnd': indexEnd,
            'thresholdLo': thresholdLo, 'thresholdHi': thresholdHi, 'winLength': winLength}


@pytest.mark.parametrize('test_name,input_dict,expected', [
    ('basic test', input_args_2t_rev(), 9),
    ('higher threshold', input_args_2t_rev(thresholdHi=5.1), 9),
    ('at higher threshold', input_args_2t_rev(thresholdHi=5.0), 9),
    ('small window', input_args_2t_rev(winLength=1), 9),
    ('larger window', input_args_2t_rev(thresholdHi=5.1, winLength=3), 6),
    ('too large window', input_args_2t_rev(winLength=4), None),
    ('further end index', input_args_2t_rev(indexBegin=12), 12),
    ('lower threshold over upper', input_args_2t_rev(thresholdLo=5), None),
    ('ending on part of window', input_args_2t_rev(indexBegin=11), 9),
    ('starting on partial window', input_args_2t_rev(indexEnd=2), 9),
])
def test_backSearchContinuityWithinRange(test_name, input_dict, expected):
    print(test_name)
    result = backSearchContinuityWithinRange(**input_dict)
    assert result == expected
    

def input_args_2d(data1=test_series, data2=neg_test_series, indexBegin=3, indexEnd=9, threshold1=0.5, threshold2=-4.5, winLength=2):
    return {'data1': data1, 'data2': data2, 'indexBegin': indexBegin, 'indexEnd': indexEnd,
            'threshold1': threshold1, 'threshold2': threshold2, 'winLength': winLength}


@pytest.mark.parametrize('test_name,input_dict,expected', [
    ('basic test', input_args_2d(), 8),
    ('higher threshold', input_args_2d(threshold2=-5.1), 4),
    ('at higher threshold', input_args_2d(threshold2=-5.0), 8),
    ('small window', input_args_2d(winLength=1), 4),
    ('too large window', input_args_2d(winLength=4), None),
    ('too large window', input_args_2d(winLength=3), None),
    ('further end index', input_args_2d(indexEnd=12), 8),
    ('ending on part of window', input_args_2d(indexEnd=11), 8),
    ('starting on partial window', input_args_2d(indexBegin=2), 8),
])
def test_searchContinuityAboveValueTwoSignals(test_name, input_dict, expected):
    print(test_name)
    assert searchContinuityAboveValueTwoSignals(**input_dict) == expected
    # all tests should work if datasets 1 and 2 are reversed
    (input_dict['data2'], input_dict['data1']) = (input_dict['data1'], input_dict['data2'])
    (input_dict['threshold2'], input_dict['threshold1']) = (input_dict['threshold1'],
                                                            input_dict['threshold2'])
    print(searchContinuityAboveValueTwoSignals(**input_dict))
    assert searchContinuityAboveValueTwoSignals(**input_dict) == expected


def input_args_2t(data=test_series, indexBegin=3, indexEnd=9,
                      thresholdLo=0.5, thresholdHi=4.5, winLength=2):
    return {'data': data, 'indexBegin': indexBegin, 'indexEnd': indexEnd,
            'thresholdLo': thresholdLo, 'thresholdHi': thresholdHi, 'winLength': winLength}


@pytest.mark.parametrize('test_name,input_dict,expected', [
    ('basic test', input_args_2t(), [(8, 9)]),
    ('higher threshold', input_args_2t(thresholdHi=5.1), [(4, 6), (8, 9)]),
    ('at higher threshold', input_args_2t(thresholdHi=5.0), [(8, 9)]),
    ('small window', input_args_2t(winLength=1), [(4, 4), (6, 6), (8, 9)]),
    ('too large window', input_args_2t(winLength=4), []),
    ('larger window', input_args_2t(thresholdHi=5.1, winLength=3), [(4, 6)]),
    ('further end index', input_args_2t(indexEnd=12), [(8, 9), (11, 12)]),
    ('lower threshold over upper', input_args_2t(thresholdLo=5), []),
    ('ending on part of window', input_args_2t(indexEnd=11), [(8, 9)]),
    ('starting on partial window', input_args_2t(indexBegin=2), [(8, 9)]),
])
def test_searchMultiContinuityWithinRange(test_name, input_dict, expected):
    print(test_name)
    result = searchMultiContinuityWithinRange(**input_dict)
    assert result == expected


if __name__ == '__main__':
    pytest.main()
