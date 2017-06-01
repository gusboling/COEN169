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
def getCosinePrediction(test_user, train_list):

    inv_ratings = getInvertedRatingsList(train_list)
    predict_user = test_user

    for target in predict_user.targets:

        if target in inv_ratings:
            target_trainers = inv_ratings[target]
            best_id = ""
            best_match = 0

            for trainer_id in target_trainers:
                similarity = getCosineSimilarity(test_user, train_list[int(trainer_id)])
                if  similarity > best_match:
                    best_match = similarity
                    best_id = trainer_id

            prediction = train_list[int(trainer_id)].get_rating(target)
            predict_user.ratings[target] = prediction

        else:
            predict_user.targets.remove(target)

    return predict_user

if __name__ == "__main__":

    training_group = dataload.training_data("./train.txt")
    testing_group = dataload.testing_data("./test5.txt")

    getCosinePrediction(testing_group[0], training_group)
