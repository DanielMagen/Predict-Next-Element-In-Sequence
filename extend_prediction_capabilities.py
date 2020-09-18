"""
this file contains multiple functions that extend the simple prediction capability
"""


def create_prediction_series(lis, predictor):
    """
    this function returns a list, lets call it p, of the length of the given lis
    such that p[i] = the prediction of the i'th element in lis given the first i-1 elements
    to make things nice, p[0] would be equal to lis[0]

    :param lis:
    :param predictor:
    :return: the prediction list created
    """
    p = [lis[0]]
    for i in range(1, len(lis)):
        p.append(predictor.predict(lis[: i]))

    return p


def get_lists_of_predictions(lis, predictor):
    """
    n = len(lis)
    this function return n-1 lists
    such that the i'th list is a predicted list, which has length n (the same length as lis)
    which was predicted from the first i + 1 element in lis

    :param lis:
    :param predictor:
    :return:
    """
    predicted_lists = []
    for i in range(1, len(lis)):
        current_list = lis[: i]
        while len(current_list) < len(lis):
            current_list.append(predictor.predict(current_list))

        predicted_lists.append(current_list)

    return predicted_lists
