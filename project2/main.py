'''
Augustus Boling
COEN 169 - Web Information Management
24 May 2017

NAME: main
DESCRIPTION: a module to provide movie recommendations based on training data.
Three test data sets are used, each with 5, 10, and 20 empyrical
ratings per user respectively.
'''

#Standard library imports
import sys

#Application imports
import dataload

def main():
    train_file = "./train.txt"
    test_files = ["./test5.txt", "./test10.txt", "./test20.txt"]

    print("[INFO] Initializing Recommendation Engine.")
    training_group = dataload.TrainingData(train_file)
    print("[INFO] Loaded data for {} training-users.".format(len(training_group)))
    print("[INFO] Nothing else to do;")
    sys.exit(0)

if __name__=="__main__":
    main()
