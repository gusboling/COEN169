'''
Augustus Boling, 2017
COEN 169 - Web Information Management
24 May 2017

NAME: models
DESCRIPTION: a library to support representing the data structures found in
both the test and training data using python classes.
'''

#Standard library imports
import math
import sys

#CLASS: TrainUser
#DESCRIPTION: a class to represent training-users
class TrainUser:

    #Constructor method; takes a user id (string) and a dict of <movie>:<rating> pairs.
    def __init__(self, new_id, new_rating_list):
        self.id = str(new_id)
        self.ratings = {}

        for index, rating in enumerate(new_rating_list):
            self.ratings[str(index+1)] = int(rating)

    #Return the rating of movie at ratings[movie_id]; returns 0 if key not valid.
    def get_rating(self, movie_id):

        if movie_id in self.ratings:
            return self.ratings[movie_id]

        return 0;

    #Return the pythagorean length of the user's rating-vector
    def length(self):

        total = 0

        for key in self.ratings:
            total = total + int(self.ratings[key])**2

        return math.sqrt(total)

    #Return the pythagorean length of the user's rating-vector
    def pearson_length(self):

        total = 0

        for key in self.ratings:
            total = total + (int(self.ratings[key]) - self.average_rating())**2

        return math.sqrt(total)

    #Of the movies the user has seen, return the average rating
    def average_rating(self):

        count = 0
        total = 0

        for key in self.ratings:
            if int(self.ratings[key]) != 0:
                count += 1
                total += int(self.ratings[key])

        return (total/count)

#CLASS: TestUser
#DESCRIPTION: a class to represent testing-users
class TestUser:
    #Constructor method; takes a user id (string) and a dict of <movie>:<rating> pairs.
    def __init__(self, new_id, new_ratings):

        self.id = str(new_id)
        self.targets = [] #The movies we want to make predictions about [<movie_id>]
        self.ratings = new_ratings #A dictionary of all rated movies {<movie_id>:<movie_rating>}

        for key in new_ratings:

            if new_ratings[key] == 0:
                self.targets.append(key)

    #Return rating of movie at ratings[movie_id] as an int; returns 0 if key not valid.
    def get_rating(self, movie_id):

        if movie_id in self.ratings:
            return int(self.ratings[movie_id])

        return 0;

    #Return a dict containing all keys with non-zero values from self.ratings
    def get_non_zero(self):
        nz = {}
        for key in self.ratings:
            if int(self.ratings[key]) != 0:
                nz[key]=int(self.ratings[key])
        return nz

    #Return the pythagorean length of the user's rating-vector as a float
    def length(self):

        total = 0

        for key in self.ratings:
            total = total + int(self.ratings[key])**2

        return math.sqrt(total)

    #Return the pythagorean length of the user's rating-vector
    def pearson_length(self):

        total = 0

        for key in self.ratings:
            total = total + (int(self.ratings[key]) - self.average_rating())**2

        return math.sqrt(total)

    #Of the movies the user has seen, return the average rating
    def average_rating(self):

        count = 0
        total = 0

        for key in self.ratings:
            if int(self.ratings[key]) != 0:
                count += 1
                total += int(self.ratings[key])

        return (total/count)

    #Add a movie/rating pair to the user's rating dictionary
    def add_rating(self, movie_id, rating):

        self.ratings[movie_id] = int(rating)

        if rating == 0:
            self.targets.append(movie_id)
