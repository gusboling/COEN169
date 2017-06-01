'''
Augustus Boling
COEN 169 - Web Information Management
24 May 2017

NAME: datawrite
DESCRIPTION: a module to provide writing predictions back to file in appropriate format
'''

def writePredictions(test_list, output_path):
    with open(output_path, "w") as out_file:
        for tester_obj in test_list:
            for movie_id in tester_obj.ratings:

                #paranoid unit-test/constraint enforcement (likely redundant)
                output_ratings = tester_obj.ratings[movie_id]
                if output_ratings < 1:
                    output_ratings = 1
                elif output_ratings > 5:
                    output_ratings = 5

                out_file.write("{} {} {}\n".format(tester_obj.id, movie_id, output_ratings))
