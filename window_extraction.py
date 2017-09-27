import pytest
import pandas
import numpy


def import_data():
    batting_file_path = 'latestSwing.csv'
    try:
        batting_data_df = pandas.read_csv(batting_file_path)
    except FileNotFoundError:
        text = '{} is not stored in this repo and needs to be manually added'.format(batting_file_path)
        raise FileNotFoundError(text)
    column_names = ['time', 'ax', 'ay', 'az', 'wx', 'wy', 'wz']
    batting_data_df.columns = column_names
    simple_structure = {}
    for column_name in column_names:
        simple_structure[column_name] = numpy.array(batting_data_df[column_name])
    return simple_structure


def first_window_in_data(data, index_iter, threshold_function, winLength):
    start_idx = None
    for idx in index_iter:
        point = data[idx]
        if threshold_function(point):
            if start_idx is None:
                start_idx = idx
            last_idx = idx
        else:
            if start_idx is not None:
                if abs(last_idx - start_idx) >= winLength - 1:
                    return start_idx, idx - 1
            start_idx = None
            last_idx = None
    if start_idx is not None:
        if abs(last_idx - start_idx) >= winLength - 1:
            return start_idx, idx


def searchContinuityAboveValue(data, indexBegin, indexEnd, threshold, winLength):
    """
    Returns the starting index of the first window of data within the target indices that
    this continuously above the threshold for winLength points
    :param data: The list, series or array of real numbers to be analyzed
    :param indexBegin: The first index to be analyzed within data
    :param indexEnd: The last index in the section of data to be analyzed
    :param threshold: The exclusive minimum value at which points are excluded
    :param winLength: The number of datapoints required for a window to be considered
    :return: integer index of the first window that meets all input criteria (e.g. 8)
             returns None if no valid windows are found
    """
    index_iter = range(indexBegin, indexEnd+1)
    threshold_function = lambda x: x > threshold
    first_window = first_window_in_data(data, index_iter, threshold_function, winLength)
    if first_window:
        return first_window[0]


def backSearchContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """
    Returns the starting index of the first window of data within the target indices that
    this continuously above the threshold for winLength points searching backwards from the end
    of the data set
    :param data: The list, series or array of real numbers to be analyzed
    :param indexBegin: The first index to be analyzed within data (will be greater than indexEnd)
    :param indexEnd: The last index in the section of data to be analyzed
    :param thresholdLo: The exclusive minimum value at which points are excluded
    :param thresholdHi: The exclusive maximum value at which points are included
    :param winLength: The number of datapoints required for a window to be considered
    :return: integer index of the first window (searchiing backwards) that meets all input criteria (e.g. 8)
             returns None if no valid windows are found
    """
    index_iter = range(indexBegin, indexEnd-1, -1)
    threshold_function = lambda x: thresholdLo < x and x < thresholdHi
    first_window = first_window_in_data(data, index_iter, threshold_function, winLength)
    if first_window:
        return first_window[0]


def searchContinuityAboveValueTwoSignals(data1, data2, indexBegin, indexEnd,
                                         threshold1, threshold2, winLength):
    """
    Returns the starting index of the first window of data within the target indices that
    this continuously above the threshold for winLength points
    :param data1: The first list, series or array of real numbers to be analyzed
    :param data2: The second list, series or array of real numbers to be analyzed
    :param indexBegin: The first index to be analyzed within data
    :param indexEnd: The last index in the section of data to be analyzed
    :param threshold1: The exclusive minimum value at which points in data1 are excluded
    :param threshold2: The exclusive minimum value at which points in data2 are excluded
    :param winLength: The number of datapoints required for a window to be considered
    :return: integer index of the first window that meets all input criteria (e.g. 8)
             returns None if no valid windows are found
    """
    data = list(zip(data1, data2))
    index_iter = range(indexBegin, indexEnd+1)
    threshold_function = lambda x: threshold1 < x[0] and threshold2 < x[1]
    first_window = first_window_in_data(data, index_iter, threshold_function, winLength)
    if first_window:
        return first_window[0]


def searchMultiContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """
    Returns all regions of data within the target indices that are continuously within the target
    thresholds for winLength points or more
    :param data: The list, series or array of real numbers to be analyzed
    :param indexBegin: The first index to be analyzed within data
    :param indexEnd: The last index in the section of data to be analyzed
    :param thresholdLo: The exclusive minimum value at which points are excluded
    :param thresholdHi: The exclusive maximum value at which points are included
    :param winLength: The number of datapoints required for a window to be include in the outut list
    :return: list of tuples containing the start and end index of the windows found
            e.g. [(1,4), (6,8)]
    """

    threshold_function = lambda x: thresholdLo < x and x < thresholdHi
    window_found = True
    windows = []
    start_idx = indexBegin
    while window_found:
        index_iter = range(start_idx, indexEnd + 1)
        window_found = first_window_in_data(data, index_iter, threshold_function, winLength)
        if window_found:
            windows.append(window_found)
            start_idx = window_found[1] + 1
    return windows


if __name__ == '__main__':
    pytest.main()
