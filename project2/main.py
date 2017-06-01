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
import datawrite
import models
import predict

#FUNCTION: loadTrainingData
#DESCRIPTION: takes a filepath as a string and returns a list of TrainUser objects
#   along with printing informational messages.
def loadTrainingData(train_path):

    training_list = dataload.training_data(train_path)
    print("[LOAD] Loaded data for {} training users.".format(len(training_list)))
    return training_list

#FUNCTION: loadTestingData
#DESCRIPTION: takes a filepath as a string and returns a list of TestUser objects
#   along with printing informational messages.
def loadTestingData(test_path):

    test_list = dataload.testing_data(test_path)
    nz_ratings = len(test_list[0].get_non_zero())
    print("[LOAD] Loaded data for {} test users (~{} sample ratings).".format(len(test_list), nz_ratings))
    return test_list

#FUNCTION: main
#DESCRIPTION: the main execution block for Project 2
def main():

    train_file = "./train.txt"
    test_files = ["./test5.txt", "./test10.txt", "./test20.txt"]
    print("[INFO] Initializing Recommendation Engine.")

    #PHASE 1: Read in data from text files and convert it into python data-structures
    trainers = loadTrainingData(train_file)

    testers_5 = loadTestingData(test_files[0])
    testers_10 = loadTestingData(test_files[1])
    testers_20 = loadTestingData(test_files[2])

    predict_5 = []
    predict_10 = []
    predict_20 = []

    #PHASE 2: Make predictions for each user using cosine-similarity and output results
    tpc = 0
    for tester in testers_5:
        print("[DEBUG] len(testers_5)")
        if (tpc % 10) == 0:
            print("[INFO] Processed {}/{} in testers_5".format(tpc, len(testers_5)))
        predict_5.append(predict.getCosinePrediction(tester, trainers))
        tpc += 1

    print("[DEBUG] len(testers_5):{}, len(predict_5):{}".format(len(testers_5), len(predict_5)))
    datawrite.writePredictions(predict_5, "predict_5.txt")
    print("[INFO] Wrote results to file.")

    '''
    tpc = 0
    for tester in testers_10:
        if (tpc % 10) == 0:
            print("[INFO] Processed {}/{} in testers_10".format(tpc, len(testers_10)))
        predict_10.append(predict.getCosinePrediction(tester, trainers))
        tpc += 1
    datawrite.writePredictions(predict_10, "predict_10.txt")
    print("[INFO] Wrote results to file.")

    tpc = 0
    for tester in testers_20:
        if (tpc % 10) == 0:
            print("[INFO] Processed {}/{} in testers_20".format(tpc, len(testers_20)))
        predict_20.append(predict.getCosinePrediction(tester, trainers))
        tpc += 1
    datawrite.writePredictions(predict_20, "predict_20.txt")
    print("[INFO] Wrote results to file.")
    '''


    #PHASE 3: Make predictions for each user using pearson-similarity and output results

    #PHASE 4: Make predictions for each user using a third method and output results

    print("[INFO] Nothing else to do;")
    sys.exit(0)

if __name__=="__main__":

    main()
