#!/usr/local/bin/python
import pytest
import pandas


def import_data():
    batting_file_path = 'latestSwing.csv'
    try:
        batting_data_df = pandas.read_csv(batting_file_path)
    except FileNotFoundError:
        text = '{} is not stored in this repo and needs to be manually added'.format(batting_file_path)
        raise FileNotFoundError(text)
    column_names = ['time', 'ax', 'ay', 'az', 'wx', 'wy', 'wz']
    batting_data_df.columns = column_names
    return batting_data_df


def searchContinuityAboveValue(data, indexBegin, indexEnd, threshold, winLength):
    """return start of section that is over the window size"""
    subseries = data[indexBegin:indexEnd+1]
    filtered_series = subseries[subseries > threshold]
    start_idx = None
    last_idx = None
    for idx, point in filtered_series.iteritems():
        if start_idx is None:
            start_idx = idx
        elif idx != last_idx + 1:
            start_idx = idx
        last_idx = idx
        if idx == start_idx + winLength - 1:
            return start_idx
    return None


def backSearchContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """return start of section that is within the window size"""
    pass


def searchContinuityAboveValueTwoSignals(data1, data2, indexBegin, indexEnd,
                                         threshold1, threshold2, winLength):
    """Return start of section w both signals above threshold"""
    pass


def searchMultiContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """return all sections of sufficient length within range"""
    subseries = data[indexBegin:indexEnd+1]
    filtered_series = subseries[(thresholdLo < subseries) & (subseries < thresholdHi)]
    start_idx = None
    last_idx = None
    output_ranges = []
    for idx, point in filtered_series.iteritems():
        if start_idx is None:
            start_idx = idx
        elif idx != last_idx + 1:
            if last_idx - start_idx > winLength - 1:
                output_ranges.append((start_idx, last_idx))
            start_idx = idx
        last_idx = idx
    # checking if the last entry was part of a large enough section
    if last_idx - start_idx >= winLength - 1:
        output_ranges.append((start_idx, last_idx))
    return output_ranges


if __name__ == '__main__':
    pytest.main()
