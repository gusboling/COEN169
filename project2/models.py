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

class User:
    def __init__(self, new_user_id, new_rating_list):
        if None in [new_user_id, new_rating_list]:
            print("[ERROR] NoneType argument passed to model constructor.")
            sys.exit(1)
        self.userid = new_user_id
        self.ratinglist = new_rating_list

    def ratings_count(self):
        return len(self.ratinglist)

    def to_string(self):
        return "({}, {})".format(self.userid, len(self.ratinglist))
