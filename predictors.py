from abstract_prediction_methods import *
from fractions import Fraction
from definitions import TYPE_LIST
import math


class AbstractStaticPredictor:
    """
    this class is an abstract base class for the implementation of static prediction classes.
    for now this is the only base case, but it might be necessary to create non static base classes as well
    in the future.
    """

    def get_name(self):
        return type(self).__name__

    def get_base_case_number(self, lis):
        """
        :param lis:
        :return: returns a number, call it x,
        such that inference_function(lis, x) would be the predicted next element in lis.
        i.e. since we reached our base case we can easily just give that number back without any further reductions.

        we separated this from the base case function in order for us to be able to get the base case number
        at will
        """
        pass

    def base_case(self, lis):
        """
        :param lis:
        :return:
        if the given list does not answers to the base case it returns None.

        otherwise it returns the result from get_base_case_number
        """
        pass

    def reduce_function(self, lis):
        """
        :param lis:
        :return: another list that would be fed to the reduce_function next.
        generally the list returned would be closer to the base case than the list given
        """
        pass

    def inference_function(self, lis, predicted_next_element_of_reduced_lis):
        """
        :param lis:
        :param predicted_next_element_of_reduced_lis:
        :return: given that we got the next predicted element in the reduced list, return the predicted next element
        in that list
        """
        pass

    def get_sublist_which_can_be_predicted(self, lis):
        """
        :param lis:
        :return:
        the list given might contain some elements that interfere with the prediction and as such needs to be removed
        this returns a sublist that must contain the last element in the list that can be predicted.

        if no such sublist can be achieved it returns an empty list

        """
        # default to returning the whole list.
        return lis

    def predict(self, lis):
        """

        :param lis:
        :return: if the list can be used to predict its next element it returns the predicted element.
        otherwise it returns None
        """
        sublist_to_predict = self.get_sublist_which_can_be_predicted(lis)
        if len(sublist_to_predict) == 0:
            return None
        return predict_next_element(sublist_to_predict,
                                    self.base_case,
                                    self.reduce_function,
                                    self.inference_function)


class Division(AbstractStaticPredictor):
    def get_base_case_number(self, lis):
        # lis contains only 1 element so we assume that the series is constant
        # as such we want our inference_function to return lis[-1]
        # so we solve for lis[-1] * x = lis[-1]
        # and return x
        return 1

    def base_case(self, lis):
        if len(lis) == 1 or 0 in lis:
            return self.get_base_case_number(lis)
        return None

    def reduce_function(self, lis):
        return [lis[i] / lis[i - 1] for i in range(1, len(lis))]

    def inference_function(self, lis, predicted_next_element_of_reduced_lis):
        return lis[-1] * predicted_next_element_of_reduced_lis

    def get_sublist_which_can_be_predicted(self, lis):
        try:
            last_occurrence_of_zero = len(lis) - lis[::-1].index(0)
        except:
            return lis

        return lis[last_occurrence_of_zero + 1:]


class DivisionFrac(Division):
    # empirically gives the same results as the regular Division once you convert to float
    def reduce_function(self, lis):
        return [Fraction(lis[i], lis[i - 1]) for i in range(1, len(lis))]


class ImprovedDivision(Division):
    """
    when tested on oeis:

    ImprovedDivision
    skipped 13386
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 268622 | 51496  |
    |      2       | 241871 | 78247  |
    |     1.1      | 175680 | 144438 |
    |     1.01     | 102621 | 217497 |
    |    1.001     | 60209  | 259909 |
    |  1.0000001   | 19897  | 300221 |
    |      1       | 10918  | 309200 |
    +--------------+--------+--------+
    """

    minimum_allowed_number = 0.6666666667  # it seems like for any lower than 2/3 the precision drops for some reason

    def reduce_function(self, lis):
        # for some reason if we move the checking to the base case instead the precision drops.
        # so the moment we see a number smaller than 2/3 we know that our function messed up and can not proceed
        # with the current results
        to_return = super().reduce_function(lis)
        if min(map(abs, to_return)) < self.minimum_allowed_number:
            return [1]
        return to_return


class DivisionCanDealWithZero(Division):
    def base_case(self, lis):
        if len(lis) == 1:
            return self.get_base_case_number(lis)
        return None

    def reduce_function(self, lis):
        to_return = [lis[i] / lis[i - 1] if lis[i - 1] != 0 else None for i in range(1, len(lis))]
        max_in_to_return = -float('inf')
        for item in to_return:
            if item is not None and item > max_in_to_return:
                max_in_to_return = item

        if max_in_to_return == -float('inf'):
            # the list was all zeros
            return [self.get_base_case_number(lis)]

        for i in range(len(to_return)):
            if to_return[i] is None:
                to_return[i] = max_in_to_return

        return to_return

    def get_sublist_which_can_be_predicted(self, lis):
        return lis


class ImprovedDivisionCanDealWithZero(DivisionCanDealWithZero):
    """
    ImprovedDivisionCanDealWithZero
    skipped 9
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 272015 | 61480  |
    |      2       | 243389 | 90106  |
    |     1.1      | 176240 | 157255 |
    |     1.01     | 104270 | 229225 |
    |    1.001     | 63291  | 270204 |
    |  1.0000001   | 24856  | 308639 |
    |      1       | 15290  | 318205 |
    +--------------+--------+--------+
    """
    minimum_allowed_number = 0.6666666667  # it seems like for any lower than 2/3 the precision drops for some reason

    def reduce_function(self, lis):
        # for some reason if we move the checking to the base case instead the precision drops.
        # so the moment we see a number smaller than 2/3 we know that our function messed up and can not proceed
        # with the current results
        to_return = super().reduce_function(lis)
        if min(map(abs, to_return)) < self.minimum_allowed_number:
            return [1]
        return to_return


class ImprovedDivisionFrac(ImprovedDivision):
    # empirically gives the same results as the regular ImprovedDivision once you convert to float
    def reduce_function(self, lis):
        return [Fraction(lis[i], lis[i - 1]) for i in range(1, len(lis))]


class Subtraction(AbstractStaticPredictor):
    """
    when tested on oeis:

    Subtraction
    skipped 9
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 82253  | 251242 |
    |      2       | 65540  | 267955 |
    |     1.1      | 39176  | 294319 |
    |     1.01     | 26210  | 307285 |
    |    1.001     | 17433  | 316062 |
    |  1.0000001   |  8664  | 324831 |
    |      1       |  7211  | 326284 |
    +--------------+--------+--------+
    """

    def get_base_case_number(self, lis):
        # lis contains only 1 element so we assume that the series is constant
        # as such we want our inference_function to return lis[-1]
        # so we solve for lis[-1] + x = lis[-1]
        # and return x
        return 0

    def base_case(self, lis):
        if len(lis) == 1:
            return self.get_base_case_number(lis)
        return None

    def reduce_function(self, lis):
        return [lis[i] - lis[i - 1] for i in range(1, len(lis))]

    def inference_function(self, lis, predicted_next_element_of_reduced_lis):
        return lis[-1] + predicted_next_element_of_reduced_lis


class TruncationWrapperCreator(type):
    """
    wraps base classes and create new subclass such that the results they return are truncated after the decimal point
    by the amount we choose.

    the idea behind this wrapper is that maybe truncating the results along the way by some amount would
    get rid of some "noise" that obstructs the prediction
    """

    @staticmethod
    def truncate_float(float_number, truncation_value):
        if truncation_value == -1:
            return float_number
        return float(f"%.{truncation_value}f" % float_number)

    @staticmethod
    def truncate_array(array_of_floats, truncation_value):
        return list(map(lambda x: TruncationWrapperCreator.truncate_float(x, truncation_value), array_of_floats))

    @classmethod
    def create_wrapper(cls, function_to_wrap, method_to_apply_on_output_of_function):
        def wrapped(*args, **kwargs):
            res = method_to_apply_on_output_of_function(function_to_wrap(*args, **kwargs))
            return res

        return wrapped

    def __init__(cls, classname, bases, class_dict):
        """
        creates subclasses that in their init function should get a truncation_value
        each number returned from the class functions would be truncated
        :param classname:
        :param bases:
        :param class_dict:
        """

        # all the class attrs can be seen in dir(cls)

        def __init__(self, truncation_value):
            self.truncation_value = truncation_value

        setattr(cls, '__init__', __init__)

        def base_case(self, *args):
            to_return = super(cls, self).base_case(*args)
            if to_return is None:
                return to_return
            return TruncationWrapperCreator.truncate_float(to_return, self.truncation_value)

        setattr(cls, 'base_case', base_case)

        # reduce_function_attr = getattr(cls, 'reduce_function')
        def reduce_function(self, *args):
            return TruncationWrapperCreator.truncate_array(super(cls, self).reduce_function(*args),
                                                           self.truncation_value)

        setattr(cls, 'reduce_function', reduce_function)

        # inference_function_attr = getattr(cls, 'inference_function')
        def inference_function(self, *args):
            return TruncationWrapperCreator.truncate_float(super(cls, self).inference_function(*args),
                                                           self.truncation_value)

        setattr(cls, 'inference_function', inference_function)

        super(TruncationWrapperCreator, cls).__init__(classname, bases, class_dict)


# create new classes with truncation
DivisionWithTruncation = TruncationWrapperCreator("DivisionWithTruncation", (Division,), {})
ImprovedDivisionWithTruncation = TruncationWrapperCreator("ImprovedDivisionWithTruncation", (ImprovedDivision,), {})


class SlopeAndBias(AbstractStaticPredictor):
    """
    assume that a_{n+1} = a_{n} * m + b  and predict a_{n+1} through predicting m,b
    """

    """
    when tested on oeis:
    seems to be overall worse than ImprovedDivisionCanDealWithZero but there are some lists which are exactly
    of the form of slope and bias and hence it catches them and is better in the 'error margin of 1' case
    
    SlopeAndBias
    slope_predictor: ImprovedDivisionCanDealWithZero
    bias_predictor: Subtraction
    skipped 9
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 256691 | 76804  |
    |      2       | 227234 | 106261 |
    |     1.1      | 149241 | 184254 |
    |     1.01     | 63356  | 270139 |
    |    1.001     | 36572  | 296923 |
    |  1.0000001   | 26245  | 307250 |
    |      1       | 24387  | 309108 |
    +--------------+--------+--------+
    
    SlopeAndBias
    slope_predictor: ImprovedDivisionCanDealWithZero
    bias_predictor: ImprovedDivisionCanDealWithZero
    skipped 9
    +--------------+--------+--------+
    | error margin | passed | failed |
    +--------------+--------+--------+
    |      5       | 271569 | 61926  |
    |      2       | 242197 | 91298  |
    |     1.1      | 169122 | 164373 |
    |     1.01     | 96302  | 237193 |
    |    1.001     | 61333  | 272162 |
    |  1.0000001   | 36305  | 297190 |
    |      1       | 25394  | 308101 |
    +--------------+--------+--------+
    """

    class_for_slope_prediction = ImprovedDivisionCanDealWithZero
    class_for_bias_prediction = ImprovedDivisionCanDealWithZero

    class_to_create_slopes = ImprovedDivisionCanDealWithZero

    def __init__(self):
        self.slope_predictor = self.class_for_slope_prediction()
        self.bias_predictor = self.class_for_bias_prediction()

        self.slopes_creator = self.class_to_create_slopes()

    def get_name(self):
        return type(self).__name__ \
               + '\n' \
               + "slope_predictor: " + self.slope_predictor.get_name() \
               + '\n' \
               + "bias_predictor: " + self.bias_predictor.get_name()

    def convert_list_to_slopes_and_biases(self, lis):
        # first check if the list given can even be processed
        # it it answers to base conditions of either the slope_predictor or the bias_predictor
        # then we just need to return the base numbers for each class

        result_from_slope_base_check = self.slope_predictor.base_case(lis)
        result_from_biases_base_check = self.bias_predictor.base_case(lis)

        if result_from_slope_base_check is not None or result_from_biases_base_check is not None:
            slope_base_number = self.slope_predictor.get_base_case_number(lis)
            biases_base_number = self.bias_predictor.get_base_case_number(lis)
            return [[slope_base_number], [biases_base_number]]

        slopes = list(map(math.floor, self.slopes_creator.reduce_function(lis)))
        biases = [lis[i + 1] - (lis[i] * slopes[i]) for i in range(len(slopes))]

        return [slopes, biases]

    def get_base_case_number(self, lis):
        if type(lis[0]) is TYPE_LIST:
            # lis is a list of both slopes and biases
            slopes, biases = lis
        else:
            slopes, biases = self.convert_list_to_slopes_and_biases(lis)

        slope_base_number = self.slope_predictor.get_base_case_number(slopes)
        biases_base_number = self.bias_predictor.get_base_case_number(biases)
        return [slope_base_number, biases_base_number]

    def base_case(self, lis):
        if type(lis[0]) is TYPE_LIST:
            # lis is the list of both slopes and biases
            slopes, biases = lis
        else:
            # we are at the start of the base_case checking and were given the original list
            slopes, biases = self.convert_list_to_slopes_and_biases(lis)

        result_from_slope_base_check = self.slope_predictor.base_case(slopes)
        result_from_biases_base_check = self.bias_predictor.base_case(biases)

        if result_from_slope_base_check is not None or result_from_biases_base_check is not None:
            return self.get_base_case_number(lis)

        return None

    def reduce_function(self, lis):
        if type(lis[0]) is TYPE_LIST:
            reduced_slopes = self.slope_predictor.reduce_function(lis[0])
            reduced_biases = self.bias_predictor.reduce_function(lis[1])
            return [reduced_slopes, reduced_biases]

        else:
            # we are at the start of the reduction and were given the original list
            # simply convert it to a list slopes and biases
            return self.convert_list_to_slopes_and_biases(lis)

    def inference_function(self, lis, predicted_next_element_of_reduced_lis):
        if type(lis[0]) is TYPE_LIST:
            predicted_slope, predicted_bias = predicted_next_element_of_reduced_lis
            inferred_slope = self.slope_predictor.inference_function(lis[0], predicted_slope)
            inferred_bias = self.bias_predictor.inference_function(lis[1], predicted_bias)
            return [inferred_slope, inferred_bias]

        else:
            # we are at the end of the inference and were given the original list
            slope, bias = predicted_next_element_of_reduced_lis
            return (lis[-1] * slope) + bias

    def get_sublist_which_can_be_predicted(self, lis):
        return self.slopes_creator.get_sublist_which_can_be_predicted(lis)
