from testing_on_oeis.load_oeis_series_helper import get_oeis_sequences
from prettytable import PrettyTable


def test_if_prediction_is_correct(predictor, lis, list_of_error_margins):
    """
    :param lis:
    :param list_of_error_margins: each error margin should be >= 1
    :return:
    if the predictor can not be used to predict the next element in the list it returns None

    otherwise,
    for each error margin in the list given,
    check if the predictions of the last element are up to to the error margin
    it returns a list of booleans indicating whether this is the case
    """
    res = predictor.predict(lis[: -1])
    if res is None:
        return None

    to_return = []
    for error_margin in list_of_error_margins:
        to_return.append(lis[-1] / error_margin <= res <= lis[-1] * error_margin)
    return to_return


def t_prediction_function(list_of_predictors,
                          list_of_error_margins,
                          directory_containing_oeis_file='',
                          limit_number_of_seqs_to_load=float('inf')):
    sequences = get_oeis_sequences(directory_containing_oeis_file=directory_containing_oeis_file,
                                   limit_number_of_seqs_to_load=limit_number_of_seqs_to_load)

    for predictor in list_of_predictors:
        print()
        error_margins_map = {e: {'passed': 0, 'failed': 0} for e in list_of_error_margins}

        count_skipped = 0
        for seq in sequences:
            test_correctness = test_if_prediction_is_correct(predictor, seq, list_of_error_margins)
            if test_correctness is None:
                count_skipped += 1
                continue
            for i in range(len(test_correctness)):
                if test_correctness[i]:
                    error_margins_map[list_of_error_margins[i]]["passed"] += 1
                else:
                    error_margins_map[list_of_error_margins[i]]["failed"] += 1

        print(predictor.get_name())
        # print the results in a pretty table
        print(f'skipped {count_skipped}')
        column_names = ['error margin', 'passed', 'failed']
        results_table = PrettyTable(column_names)
        for e in list_of_error_margins:
            results_table.add_row([e, error_margins_map[e]["passed"], error_margins_map[e]["failed"]])
        print(results_table)
