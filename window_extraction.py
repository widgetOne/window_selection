#!/usr/local/bin/python
import os
import pandas


def import_data():
    batting_file_path = 'latestSwing.csv'
    batting_data_df = pandas.read_csv(batting_file_path)
    return batting_data_df


def searchContinuityAboveValue(data, indexBegin, indexEnd, threshold, winLength=1):
    """return start of section that is over the window size"""
    pass


def backSearchContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength=1):
    """return start of section that is within the window size"""
    pass


def searchContinuityAboveValueTwoSignals(data1, data2, indexBegin, indexEnd, threshold1, threshold2, winLength=1):
    """Return start of section w both signals above threshold"""
    pass


def searchMultiContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength=1):
    """return all sections within range"""
    pass


if __name__ == '__main__':
    import_data()