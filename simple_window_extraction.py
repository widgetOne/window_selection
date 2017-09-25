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
    start_idx = None
    for idx in range(indexBegin, indexEnd+1):
        point = data[idx]
        if point > threshold:
            if start_idx is None:
                start_idx = idx
            if idx - start_idx >= winLength - 1:
                return start_idx
        else:
            start_idx = None


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
    start_idx = None
    for idx in range(indexBegin, indexEnd-1, -1):
        point = data[idx]
        if thresholdLo < point and point < thresholdHi:
            if start_idx is None:
                start_idx = idx
            if start_idx - idx >= winLength - 1:
                return start_idx
        else:
            start_idx = None


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
    start_idx = None
    for idx in range(indexBegin, indexEnd+1):
        point1 = data1[idx]
        point2 = data2[idx]
        if threshold1 < point1 and threshold2 < point2:
            if start_idx is None:
                start_idx = idx
            if idx - start_idx >= winLength - 1:
                return start_idx
        else:
            start_idx = None


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
    windows = []
    start_idx = None
    for idx in range(indexBegin, indexEnd+1):
        point = data[idx]
        if thresholdLo < point and point < thresholdHi:
            if start_idx is None:
                start_idx = idx
        else:
            if start_idx is not None:
                if (idx - 1) - start_idx >= winLength - 1:
                    windows.append((start_idx, idx - 1))
            start_idx = None
    if start_idx is not None:
        if indexEnd - start_idx >= winLength - 1:
            windows.append((start_idx, indexEnd))
    return windows


if __name__ == '__main__':
    pytest.main()
