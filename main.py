from predictors import *
from extend_prediction_capabilities import *


def round_list(lis):
    return list(map(lambda item: round(item), lis))


def get_fibonacci_numbers(n):
    fibonacci_numbers = [1 for _ in range(n)]

    if n < 3:
        return fibonacci_numbers

    for i in range(2, len(fibonacci_numbers)):
        fibonacci_numbers[i] = fibonacci_numbers[i - 1] + fibonacci_numbers[i - 2]
    return fibonacci_numbers


def see_predictions_results(lis, predictor):
    print("original list")
    print(lis)
    print()

    print("the predicted next element in the list")
    print(round(predictor.predict(lis)))
    print()

    print('prediction_series')
    print(round_list(create_prediction_series(lis, predictor)))
    print()

    print('lists_of_predictions')
    lists_of_predictions = get_lists_of_predictions(lis, predictor)
    for l in lists_of_predictions:
        print(round_list(l))


if __name__ == "__main__":
    lis = get_fibonacci_numbers(10)
    print("original list")
    print(lis)
    print()

    predictor_class = SlopeAndBias
    predictor = predictor_class()

    print("the predicted next element in the list")
    print(predictor.predict(lis))
    print()
