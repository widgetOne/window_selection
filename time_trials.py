#!/usr/local/bin/python
import datetime


def assess_time_cost(module_name):
    if module_name == 'window_extraction':
        import window_extraction as local_module
    elif module_name == 'simple_window_extraction':
        import simple_window_extraction as local_module
    else:
        raise Exception('Unknown module.')

    def test_data_for_array_of_thresholds(data):
        mean = data.mean()
        std_dev = data.std()
        sections = 100
        window_size = 5
        thresholds = [mean + std_dev * (idx - sections / 2) / sections for idx in range(sections)]
        min_thresholds = [mean + std_dev * (idx - sections / 2 - sections / 14) / sections for idx in range(sections)]
        max_thresholds = [mean + std_dev * (idx - sections / 2 + sections / 14) / sections for idx in range(sections)]

        for threshold in thresholds:
            local_module.searchContinuityAboveValue(data, 0, len(data), threshold, window_size)
        for low_threshold, high_threshold in zip(min_thresholds, max_thresholds):
            local_module.backSearchContinuityWithinRange(data, len(data), 0, low_threshold, low_threshold, window_size)

    columns = ['ax', 'ay', 'az', 'wx', 'wy', 'wz']
    data_structure = local_module.import_data()
    start = datetime.datetime.now()
    for col in columns:
        test_data_for_array_of_thresholds(data_structure[col])
    delta = datetime.datetime.now() - start
    print('It took {} seconds to run these tests for {}'.format(delta, module_name))

if __name__ == '__main__':
    assess_time_cost('window_extraction')
    assess_time_cost('simple_window_extraction')
