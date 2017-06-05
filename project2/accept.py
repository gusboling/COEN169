'''
Augustus Boling
COEN 169 - Web Information Management
24 May 2017

NAME: accept
DESCRIPTION: a module to support basic acceptance testing for common errors
in the format of result files. Basically just a few quick sanity tests put in a
separate module so as to not interfere with code as its being tweaked.
'''

'''
AXIOM: The "main.py" module should call one function in this module at the end of
its execution. This function should execute all appropriate check_* functions.
(KISS principle)

AXIOM: The "main.py" module should only pass the path's of select files as arguments
to this module. (This module examines the contents of test files and result
files only.)

AXIOM: A single call from the "main.py" module should cause each file in question
to be read only once for all checks being done during the execution of the call.
(Such that the read data is constantacross all checks.)

AXIOM: This module supports unit checks for the format and validity of processed
test files (with predictions for unseen movies); unprocessed test-files (containing
zeroes), or training files are beyond the scope of this module.
'''

#Python Standard Libraries
import sys

#FUNCTION: load_triples
#DESCRIPTION: Takes a test file path as a string. Returns a list of user-movie-rating
#   (triples) in the file.
def load_triples(file_path):
    triples = []
    with open(file_path, "r") as test_file:
        for line in test_file:
            new_triple = line.split()
            new_triple[2] = new_triple[2].strip()
            triples.append(new_triple)
    print("[ACCEPT] Loaded {} triples from file '{}'".format(len(triples), file_path))
    return triples


#FUNCTION: file_ratings
#DESCRIPTION: Takes a file path as a string. Returns the number of ratings
#   in a test file specified by the path.
def rating_count(file_path):
    lines = []
    with open(file_path, "r") as test_file:
        lines = test_file.readlines() #one rating per line
    return len(lines)

#FUNCTION: check_rating
#DESCRIPTION: Takes a rating (post-prediction) as a string. Checks if the  following statements are
#   true with regard to the string.
#       1. string has length of 1. (check if float)
#       2. string contains a number. (check if NaN)
#       3. int(string) >= 1 (check if out-of-bounds)
#       4. int(string) <= 5 (check if out-of-bounds)
#   If any of these conditions are not true, then print an error and trigger an
#   exit.
def check_rating(rating_str):

    if len(rating_str) != 1:
        print("[ERROR][CHECK-RATING] Found rating with more than one digit ({}). Exiting.".format(rating_str))
        sys.exit(1)
    elif not any(char.isdigit() for char in rating_str):
        print("[ERROR][CHECK-RATING] Found rating with non-digit characters ({}). Exiting.".format(rating_str))
        sys.exit(1)
    elif (int(rating_str) < 1) or (int(rating_str) > 5):
        print("[ERROR][CHECK-RATING] Found rating with out-of-bounds value ({}). Exiting.".format(rating_str))
        sys.exit(1)
    else:
        return

#FUNCTION: check_conserve
#DESCRIPTION: Takes a test file's path and it's corresponding result file's path
#   as strings. If the number of ratings in the result file doesn't equal the
#   number of ratings in the result file, print an error and trigger an exit.
def check_conserve(triples_list):
    pass

#FUNCTION: check_correspond
#DESCRIPTION: Takes a test file's path and the path of the corresponding result
#   file as strings. For each user-movie (tuple) in the test file, check that the
#   same user-movie (tuple) exists in the result file. If a pair has no corresponding
#   entry in the result file, print an error and trigger an exit.
def check_correspond(triples_list):
    pass

#FUNCTION: check_preserve
#DESCRIPTION: Takes a test file's path and the path of the corresponding result
#   file as strings. For each user-movie (triple) with a non-zero rating in the
#   test file, check if the same user-movie-rating (triple) exists in the result
#   file. If no matching (triple) can be found, print an error and trigger an exit.
def check_preserve(test_path, result_path):
    pass

#FUNCTION: check_predict
#DESCRIPTION: Takes a test file's path and the path of the corresponding result
#   file as strings. For each user-movie (tuple) with a zero rating in
#   the test file, check if the same user-movie (tuple) exists and has a rating
#   greater than 0 and less than 6.
def check_predict(test_path, result_path):
    pass

#FUNCTION: do_check
#DESCRIPTION: Take a test file's path and the path of the corresponding result
#   file as strings. Call each of the above check_* functions with the test_path
#   and result_path as arguments. If all checks return without triggering an
#   exit, then output a success message and return gracefully.
def do_check(result_path):
    triples = load_triples(result_path)

    for t in triples:
        check_rating(t[2])

    print("[ACCEPT] All ratings in prediction file '{}' meet test criteria.".format(result_path))

if __name__=="__main__":
    '''
    print("[TEST] Ratings in test5.txt (8497 ratings) = {}".format(rating_count("test5.txt")))
    print("[TEST] Ratings in test10.txt (7000 ratings) = {}".format(rating_count("test10.txt")))
    print("[TEST] Ratings in test20.txt (12367 ratings) = {}".format(rating_count("test20.txt")))
    print("")

    try_rating = ""

    good_ratings = ["1", "2", "3", "4", "5"]

    for rating in good_ratings:
        check_rating(rating)
        print("[TEST] Passed check_rating test for GOOD rating ({})".format(rating))

    print("")

    bad_ratings = ["0", "2.3", "56", "123", "6", "-1", "0.2"]

    for rating in bad_ratings:
        try:
            check_rating(rating)
        except:
            print("[TEST] Failed check_rating test for BAD rating ({}).".format(rating))

    print("")

    load_triples("pearson_result5.txt")
    '''
    do_check("test5.txt", "pearson_result5.txt")
