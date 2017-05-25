'''
Augustus Boling, 2017
COEN 169 - Web Information Management
24 May 2017

NAME: models
DESCRIPTION: a library to support representing the data structures found in
both the test and training data using python classes.
'''

#Standard library imports
import sys

class TrainUser:
    #Constructor method; takes a user id (string) and a dict of <movie>:<rating> pairs.
    def __init__(self, new_id, new_rating_list):
        self.id = str(new_id)
        self.ratings = {}
        for index, rating in enumerate(new_rating_list):
            self.ratings[index] = rating

    #Return the rating of movie at ratings[movie_id]; returns 0 if key not valid.
    def get_rating(self, movie_id):
        if movie_id in self.ratings:
            return self.ratings[movie_id]
        return 0;

class TestUser:
    #Constructor method; takes a user id (string) and a dict of <movie>:<rating> pairs.
    def __init__(self, new_id, new_ratings):
        self.id = str(new_id)
        self.targets = [] #The movies we want to make predictions about [<movie_id>]
        self.ratings = new_ratings #A dictionary of all rated movies {<movie_id>:<movie_rating>}
        for key in new_ratings:
            if new_ratings[key] == 0:
                self.targets.append(key)

    #Return the rating of movie at ratings[movie_id]; returns 0 if key not valid.
    def get_rating(self, movie_id):
        if movie_id in self.ratings:
            return self.ratings[movie_id]
        return 0;

    def add_rating(self, movie_id, rating):
        self.ratings[movie_id] = rating
        if rating == 0:
            self.targets.append(movie_id)
