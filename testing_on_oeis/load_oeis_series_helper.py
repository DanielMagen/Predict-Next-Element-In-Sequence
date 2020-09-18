import os
from ast import literal_eval


def extract_sequence_from_line(line):
    """

    :param line: of the form 'A000001 ,0,1,1,1,2,1,2,1,5,2,2,1,5,1,2,1,14,1,5,1,5...'
    :return: the name and the series in the
    """
    separator_between_name_and_series = ' '
    name, series = line.split(separator_between_name_and_series)

    # to prevent compilation errors
    if series[0] == ',':
        series = series[1:]

    series = literal_eval('[' + series + ']')
    return name, series


def line_is_comment_line(line):
    return line.startswith('#')


def extract_all_sequences_from_stripped_file(path_to_stripped_file, limit_number_of_seqs_to_load=float('inf')):
    """
    currently there are about 333-334 thousand sequences in the file
    it takes about 25 seconds to load them all
    :param path_to_stripped_file:
    :return:
    """
    seqs = []

    with open(path_to_stripped_file, 'r') as f:
        for line in f.readlines():
            if not line_is_comment_line(line):
                _, series = extract_sequence_from_line(line)
                seqs.append(series)

                limit_number_of_seqs_to_load -= 1
                if limit_number_of_seqs_to_load == 0:
                    break

    return seqs


def get_oeis_sequences(directory_containing_oeis_file='', limit_number_of_seqs_to_load=float('inf')):
    path_to_stripped_file = os.path.join(directory_containing_oeis_file, 'stripped')
    return extract_all_sequences_from_stripped_file(path_to_stripped_file, limit_number_of_seqs_to_load)
