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
#DESCRIPTION: Takes a TestUser object and a list of TrainUser objects. Returns
#   a TestUser object containing all of the non-target ratings of the argument object,
#   with predicted values for all of the argument object's target ratings (Cosine Similarity).
def getCosinePrediction(test_user, train_list):

    inv_ratings = getInvertedRatingsList(train_list)
    predict_user = test_user

    start_length_test = len(test_user.ratings)
    start_length_predict = len(predict_user.ratings)
    #print("[PREDICT][START] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    #print("[PREDICT][START] len(predict_user.ratings){}".format(len(test_user.ratings)))

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

    #print("[PREDICT][END] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    #print("[PREDICT][END] len(predict_user.ratings){}".format(len(test_user.ratings)))

    return predict_user

#FUNCTION: getPearsonSimilarity(test_user, train_user)
#DESCRIPTION: Takes a TestUser and a TrainUser object and returns their Pearson
#   similarity.
def getPearsonSimilarity(test_user, train_user):

    #calculate numerator
    numerator = 0
    for key in test_user.ratings:
        if key in train_user.ratings:
            test_delta = int(test_user.ratings[key]) - test_user.average_rating()
            train_delta = int(train_user.ratings[key]) - train_user.average_rating()
            numerator += (test_delta * train_delta)

    #calculate denominator
    denominator = test_user.pearson_length() * train_user.pearson_length()

    return numerator/denominator


    #calculate denominator

#FUNCTION: getPearsonPrediction
#DESCRIPTION: Takes a TestUser object and a list of TrainUser objects. Returns
#   a TestUser object containing all of the non-target ratings of the argument object,
#   with predicted values for all of the argument object's target ratings (Pearson Similarity).
def getPearsonPrediction(test_user, train_list):

    inv_ratings = getInvertedRatingsList(train_list) #This doesn't need to happen every time
    predict_user = test_user

    start_length_test = len(test_user.ratings)
    start_length_predict = len(predict_user.ratings)
    #print("[PREDICT][START] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    #print("[PREDICT][START] len(predict_user.ratings){}".format(len(test_user.ratings)))

    #print("[PREDICT][DEBUG] 0: {}".format(len(predict_user.ratings)))
    for target in test_user.targets:

        if target in inv_ratings:

            #print("[PREDICT][DEBUG] 1: {}".format(len(predict_user.ratings)))
            n = 15
            top_n = {}
            for trainer_id in inv_ratings[target]:
                similarity = getCosineSimilarity(test_user, train_list[int(trainer_id)])

                if len(top_n) < n:
                    top_n[trainer_id] = similarity
                else:
                    top_n[trainer_id] = similarity
                    min_sim = 1
                    min_key = str()

                    for key in top_n:
                        if min_sim > top_n[key]:
                            min_sim = top_n[key]
                            min_key = key

                    top_n.pop(min_key)

            #print("[PREDICT][DEBUG] 2: {}".format(len(predict_user.ratings)))
            total_sim = 0
            for trainer_id in top_n: total_sim += abs(int(top_n[trainer_id]))

            prediction_delta = 0
            for trainer_id in top_n:
                prediction_delta += (int(top_n[trainer_id]) * ( train_list[int(trainer_id)].ratings[target] - train_list[int(trainer_id)].average_rating() ))

            if total_sim > 0:
                prediction_delta = prediction_delta / total_sim
            else:
                prediction_delta = 0

            #print("[PREDICT][DEBUG] 3: {}".format(len(predict_user.ratings)))
            predict_user.ratings[target] = test_user.average_rating() + prediction_delta
            #print("[PREDICT][DEBUG] 3.5: {}".format(len(predict_user.ratings)))

    end_length_test = len(test_user.ratings)
    end_length_predict = len(predict_user.ratings)
    if(end_length_predict != start_length_predict) or (end_length_test != start_length_test):
        print("[PREDICT][ERROR] Failed unit test for 1:1 correspondence.")
        sys.exit(13)

    #print("[PREDICT][END] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    #print("[PREDICT][END] len(predict_user.ratings){}".format(len(test_user.ratings)))

    return predict_user

#FUNCTION: getPearsonPredictionIUF
#DESCRIPTION: Takes a TestUser object and a list of TrainUser objects. Returns
#   a TestUser object containing all of the non-target ratings of the argument object,
#   with predicted values for all of the argument object's target ratings (Pearson Similarity w/ IUF).
def getPearsonPredictionIUF(test_user, train_list):

    inv_ratings = getInvertedRatingsList(train_list)
    predict_user = test_user

    start_length_test = len(test_user.ratings)
    start_length_predict = len(predict_user.ratings)
    #print("[PREDICT][START] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    #print("[PREDICT][START] len(predict_user.ratings){}".format(len(test_user.ratings)))

    #print("[PREDICT][DEBUG] 0: {}".format(len(predict_user.ratings)))
    for target in test_user.targets:

        if target in inv_ratings:

            #print("[PREDICT][DEBUG] 1: {}".format(len(predict_user.ratings)))
            n = 10
            top_n = {}
            for trainer_id in inv_ratings[target]:
                similarity = getCosineSimilarity(test_user, train_list[int(trainer_id)])

                if len(top_n) < n:
                    top_n[trainer_id] = similarity
                else:
                    top_n[trainer_id] = similarity
                    min_sim = 1
                    min_key = str()

                    for key in top_n:
                        if min_sim > top_n[key]:
                            min_sim = top_n[key]
                            min_key = key

                    top_n.pop(min_key)

            #print("[PREDICT][DEBUG] 2: {}".format(len(predict_user.ratings)))
            total_sim = 0
            for trainer_id in top_n: total_sim += abs(int(top_n[trainer_id]))

            prediction_delta = 0
            for trainer_id in top_n:
                tid = int(trainer_id)
                IUF = math.log(len(train_list)/len(inv_ratings[target]))
                prediction_delta += (int(top_n[trainer_id]) * (train_list[tid].ratings[target] - train_list[tid].average_rating()) )

            if total_sim > 0:
                prediction_delta = (prediction_delta / total_sim) * IUF
            else:
                prediction_delta = 0

            #print("[PREDICT][DEBUG] 3: {}".format(len(predict_user.ratings)))
            predict_user.ratings[target] = test_user.average_rating() + prediction_delta
            #print("[PREDICT][DEBUG] 3.5: {}".format(len(predict_user.ratings)))

    end_length_test = len(test_user.ratings)
    end_length_predict = len(predict_user.ratings)
    if(end_length_predict != start_length_predict) or (end_length_test != start_length_test):
        print("[PREDICT][ERROR] Failed unit test for 1:1 correspondence.")
        sys.exit(13)

    #print("[PREDICT][END] len(predict_user.ratings){}".format(len(predict_user.ratings)))
    #print("[PREDICT][END] len(predict_user.ratings){}".format(len(test_user.ratings)))

    return predict_user

if __name__ == "__main__":

    training_group = dataload.training_data("./train.txt")
    testing_group = dataload.testing_data("./test5.txt")

    getCosinePrediction(testing_group[0], training_group)
    getPearsonPrediction(testing_group[0], training_group)
