import pytest
import pandas
from window_extraction import *


@pytest.fixture(scope='module')
def get_swing_data():
    batting_file_path = 'latestSwing.csv'
    batting_data = pandas.read_csv(batting_file_path)
    return batting_data


test_series = pandas.Series(['0, 1, 1, 0, 1, 5, 1, 0, 1, 2, 0, 1, 1, 0'])
default_test_input = {'data': test_series, 'indexBegin': 3, 'indexEnd': 12, 'threshold': 0.5, 'winLength': 2}
@pytest.mark.parametrize("input_dict,expected", [
    (default_test_input, 8),
])
def test_searchMultiContinuityWithinRange(input_dict, expected):
    result = searchContinuityAboveValue(**input_dict)
    assert result == expected


if __name__ == '__main__':
    pytest.main()
