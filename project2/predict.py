''''
Augustus Boling, 2017
COEN 169 - Web Information Management
1 June 2017

NAME: predict
DESCRIPTION: a library to support calculating the relative similarity of two
users, and to make predictions for unseen movies based on the result.
'''

#Python Libraries
import math
import sys

#Program Modules
import models
import dataload

#FUNCTION: getCosineSimilarity
#DESCRIPTION: Takes a TestUser object and a TrainUser object. Return the
#   cosine-similarity of two users based on their non-zero ratings
def getCosineSimilarity(test_user, train_user):
    #Initialize cross_product to 0
    cross_product = 0

    #Loop through keys in test_user.ratings
    for key in test_user.ratings:

        #If key is present in train_user.ratings, compute the product of the corresponding elements, then add them to the running total
        if key in train_user.ratings:
            cross_product = cross_product + float(int(test_user.ratings[key]) * int(train_user.ratings[key]))

    #Calculate numerator/denominator of the equation, check for zeroes
    numerator = float(cross_product)
    denominator = (test_user.length() * train_user.length())

    if denominator == 0:
        print("TestUser.length(): {}, TrainUser.length(): {}".format(test_user.length(), train_user.length()))
        result = 0
    else:
        result = numerator / denominator

    return result

#FUNCTION: getInvertedRatingsList
#DESCRIPTION: Returns a dictionary of movie ID's, each with a list of the trainers
#   that gave the movie a non-zero rating. Takes a list of TestUser objects.
def getInvertedRatingsList(train_list):
    inverted_list = {}

    for trainer in train_list:

        for key in trainer.ratings:
            if trainer.ratings[key] != 0:
                if key in inverted_list:
                    inverted_list[key].append(trainer.id)
                else:
                    inverted_list[key] = [trainer.id]


    return inverted_list

#FUNCTION: cosinePrediction
#DESCRIPTION: Takes a TrainUser object and a list of TestUser objects. Returns
#   a TestUser containing all of the non-target ratings of the argument object,
#   with predicted values for all of the argument object's target ratings.
#   k=10
def getCosinePrediction(test_user, train_list):

    inv_ratings = getInvertedRatingsList(train_list)
    predict_user = test_user

    start_length_test = len(test_user.ratings)
    start_length_predict = len(predict_user.ratings)
    print("[PREDICT][START] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    print("[PREDICT][START] len(predict_user.ratings){}".format(len(test_user.ratings)))

    #print("[PREDICT][DEBUG] 0: {}".format(len(predict_user.ratings)))
    for target in test_user.targets:

        if target in inv_ratings:
            top_10 = {}
            total_sim = 0
            predict_rating = 0

            #print("[PREDICT][DEBUG] 1: {}".format(len(predict_user.ratings)))
            for trainer_id in inv_ratings[target]:
                similarity = getCosineSimilarity(test_user, train_list[int(trainer_id)])

                if len(top_10) < 10:
                    top_10[trainer_id] = similarity
                else:
                    top_10[trainer_id] = similarity
                    min_sim = 1
                    min_key = str()

                    for key in top_10:
                        if min_sim > top_10[key]:
                            min_sim = top_10[key]
                            min_key = key

                    top_10.pop(min_key)

            #print("[PREDICT][DEBUG] 2: {}".format(len(predict_user.ratings)))
            for trainer_id in top_10: total_sim += top_10[trainer_id]

            for trainer_id in top_10:
                if total_sim != 0:
                    predict_rating += ((top_10[trainer_id]/total_sim)*train_list[int(trainer_id)].ratings[target])
                    if int(predict_rating) < 1: predict_rating = 1
                else:
                    predict_rating = 1

            #print("[PREDICT][DEBUG] 3: {}".format(len(predict_user.ratings)))
            predict_user.ratings[target] = int(predict_rating)
            #print("[PREDICT][DEBUG] 3.5: {}".format(len(predict_user.ratings)))

    end_length_test = len(test_user.ratings)
    end_length_predict = len(predict_user.ratings)
    if(end_length_predict != start_length_predict) or (end_length_test != start_length_test):
        print("[PREDICT][ERROR] Failed unit test for 1:1 correspondence.")
        sys.exit(13)

    print("[PREDICT][END] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    print("[PREDICT][END] len(predict_user.ratings){}".format(len(test_user.ratings)))

    return predict_user

if __name__ == "__main__":

    training_group = dataload.training_data("./train.txt")
    testing_group = dataload.testing_data("./test5.txt")

    getCosinePrediction(testing_group[0], training_group)
