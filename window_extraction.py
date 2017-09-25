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


def convert_index_list_to_window_tuples(index_list, winLength):
    start_idx = None
    last_idx = None
    output_ranges = []
    for idx in index_list:
        if start_idx is None:
            start_idx = idx
        elif idx != last_idx + 1:
            if last_idx - start_idx >= winLength - 1:
                output_ranges.append((start_idx, last_idx))
            start_idx = idx
        last_idx = idx
    # checking if the last entry was part of a large enough section
    if start_idx is not None and last_idx is not None and last_idx - start_idx >= winLength - 1:
        output_ranges.append((start_idx, last_idx))
    return output_ranges


def searchContinuityAboveValue(data, indexBegin, indexEnd, threshold, winLength):
    """return start of section that is over the window size"""
    subseries = data[indexBegin:indexEnd+1]
    filtered_series = subseries[subseries > threshold]
    tuple_list = convert_index_list_to_window_tuples(filtered_series.index.values, winLength)
    if len(tuple_list) > 0:
        return tuple_list[0][0]  # returning the starting index of the first acceptable window found


def backSearchContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """return start of section that is within the window size"""
    subseries = data[indexEnd:indexBegin+1]
    filtered_series = subseries[(thresholdLo < subseries) & (subseries < thresholdHi)]
    tuple_list = convert_index_list_to_window_tuples(filtered_series.index.values, winLength)
    if len(tuple_list) > 0:
        return tuple_list[-1][-1]  # returning the end of the last window


def searchContinuityAboveValueTwoSignals(data1, data2, indexBegin, indexEnd,
                                         threshold1, threshold2, winLength):
    """Return start of section w both signals above threshold"""
    subseries_1 = data1[indexBegin:indexEnd+1]
    filtered_series_1 = subseries_1[threshold1 < subseries_1]
    subseries_2 = data2[indexBegin:indexEnd+1]
    filtered_series_2 = subseries_2[threshold2 < subseries_2]
    combined_filtered_data = pandas.concat([filtered_series_1, filtered_series_2], axis=1, join='inner')
    tuple_list = convert_index_list_to_window_tuples(combined_filtered_data.index.values, winLength)
    if len(tuple_list) > 0:
        return tuple_list[0][0]  # returning the starting index of the first acceptable window found


def searchMultiContinuityWithinRange(data, indexBegin, indexEnd, thresholdLo, thresholdHi, winLength):
    """return all sections of sufficient length within range"""
    subseries = data[indexBegin:indexEnd+1]
    filtered_series = subseries[(thresholdLo < subseries) & (subseries < thresholdHi)]
    tuple_list = convert_index_list_to_window_tuples(filtered_series.index.values, winLength)
    return tuple_list


if __name__ == '__main__':
    pytest.main()
