from testing_on_oeis.testing_functions import t_prediction_function
from definitions import *
from predictors import *

if __name__ == "__main__":
    """
    instructions

    1) download the gzip file from
    https://oeis.org/wiki/Welcome#Compressed_Versions
    "There is a gzipped file containing just the sequences and their A-numbers"

    2) extract the stripped file from it and place it in the project folder
    
    3) run
    """
    list_of_predictors_classes = [SlopeAndBias, ImprovedDivisionCanDealWithZero, ImprovedDivision, Subtraction]
    list_of_predictors = [x() for x in list_of_predictors_classes]

    list_of_error_margins = [5, 2, 1.1, 1.01, 1.001, 1.0000001, 1]

    limit_number_of_seqs_to_load = float('inf')
    # limit_number_of_seqs_to_load = 100

    t_prediction_function(list_of_predictors,
                          list_of_error_margins,
                          directory_containing_oeis_file=ROOT_DIR,
                          limit_number_of_seqs_to_load=limit_number_of_seqs_to_load)
