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

def TrainingData(file_path):
    trainers = []
    with open(file_path, "r") as train_file:
        raw_ratings = train_file.readline().split()
        for i in range((len(raw_ratings)/1000)):
            user_ratings = raw_ratings[:1000]
            trainers.append(models.User(i, user_ratings))
            raw_ratings = raw_ratings[1000:]
    return trainers
