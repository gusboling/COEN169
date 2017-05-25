'''
Augustus Boling, 2017
COEN 169 - Web Information Management
24 May 2017

NAME: dataload
DESCRIPTION: a library to support reading data from training and test files,
along with some basic processing of the data.
'''
#Standard library imports
import sys

#Application imports
import models

#Function: training_data
#Returns a list of TrainUser objects
def training_data(file_path):
    trainers = []

    with open(file_path, "r") as train_file:
        raw_ratings = train_file.readline().split()
        #for every 1K ratings, create a new user and append it to the list
        for i in range((len(raw_ratings)/1000)):
            user_ratings = raw_ratings[:1000]
            trainers.append(models.TrainUser(i, user_ratings))
            raw_ratings = raw_ratings[1000:]

    return trainers

#Function: test_data
#Returns a list of TestUser objects (used for all three test files)
def test_data(file_path):
    testers = []
    users = {}

    with open(file_path, "r") as test_file:
        #for each line in test_file, split it and map the last 2 values (movie ID, rating) to the first value (user ID)
        for line in test_file:
            tokens = line.split()
            user_id = tokens[0]
            movie_id = tokens[1]
            rating = tokens[2]

            if user_id not in users:
                users[user_id] = models.TestUser(user_id, {movie_id:rating})
            else:
                users[user_id].add_rating(movie_id, rating)

    #Convert to list
    for key in users:
        testers.append(users[key])

    return testers

#Debugging Code - run when module is called from the command line w/ no arguments.
if __name__=="__main__":
    print("[DEBUG] Starting debugging execution for dataload.py")

    print("[DEBUG] Loading training data.")
    train_users = training_data("./train.txt")
    print("[DEBUG] Loaded {} training user profiles from 'train.txt'".format(len(train_users)))

    print("[DEBUG] Loading test5 data.")
    test_users = test_data("./test5.txt")
    print("[DEBUG] Loaded {} testing user profiles from 'test5.txt'.".format(len(test_users)))
