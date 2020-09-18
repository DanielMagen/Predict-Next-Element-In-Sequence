def predict_next_element_recursive(lis, base_case, reduce_function, inference_function):
    """
    :param lis: the list to predict the next element of

    :param base_case: each iteration would be given the current list. if it returns None we continue the recursion,
    otherwise we assume that the returned value is the base case for the recursion and return
    inference_function(lis, base_case(lis))

    :param reduce_function: a function that would be applied to the given list to reduce it to another (smaller?) list
    that would be fed recursively to the function

    :param inference_function: would be given the both
    lis
    and the output of
    predict_next_element(reduce_function(lis), reduce_function, inference_function) - i.e. the next element in the
    reduced list, and would give us back the next element in the list

    :return: the predicted next element in lis
    """
    if len(lis) == 0:
        return None

    base_case_result = base_case(lis)
    if base_case_result is not None:
        return inference_function(lis, base_case_result)

    reduced_list = reduce_function(lis)
    next_element_in_reduced_list = predict_next_element_recursive(reduced_list,
                                                                  base_case,
                                                                  reduce_function,
                                                                  inference_function)

    return inference_function(lis, next_element_in_reduced_list)


def predict_next_element(lis, base_case, reduce_function, inference_function):
    """
    :param lis: the list to predict the next element of

    :param base_case: each iteration would be given the current list. if it returns None we continue the recursion,
    otherwise we assume that the returned value is the base case for the recursion and return
    inference_function(lis, base_case(lis))

    :param reduce_function: a function that would be applied to the given list to reduce it to another (smaller?) list
    that would be fed recursively to the function

    :param inference_function: would be given the both
    lis
    and the output of
    predict_next_element(reduce_function(lis), reduce_function, inference_function) - i.e. the next element in the
    reduced list, and would give us back the next element in the list

    :return: the predicted next element in lis
    """
    if len(lis) == 0:
        return None

    gens = [lis]

    while True:
        base_case_result = base_case(gens[-1])
        if base_case_result is not None:
            gens.append([base_case_result])
            break
        gens.append(reduce_function(gens[-1]))

    # now predict the next element
    # the last gen contains only 1 element so we assume constant series
    predicted_next_element_of_current_gen = gens[-1][-1]

    for current_gen in range(len(gens) - 2, -1, -1):
        predicted_next_element_of_current_gen = inference_function(gens[current_gen],
                                                                   predicted_next_element_of_current_gen)

    return predicted_next_element_of_current_gen
