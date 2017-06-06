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
import timeit

#Application imports
import accept
import dataload
import datawrite
import models
import predict


def do_cosine(tester_list, trainer_list):
    tpc = 1
    results = []
    out_file = ""

    if int(tester_list[0].id) > 400:
        out_file = "cosine20"
    elif int(tester_list[0].id) > 300:
        out_file = "cosine10"
    else:
        out_file = "cosine5"

    for tester in tester_list:
        if (tpc % 10) == 0:
            print("[INFO] Processed {}/{} in {}.".format(tpc, len(tester_list), out_file))
        results.append(predict.getCosinePrediction(tester, trainer_list))
        tpc += 1
    datawrite.writePredictions(results, out_file+".txt")
    datawrite.writeCSV(results, out_file + "_csv.txt")
    print("[INFO] Wrote results to file.")
    accept.do_check(out_file + ".txt")

def do_pearson(tester_list, trainer_list):
    tpc = 1
    results = []
    out_file = ""

    if int(tester_list[0].id) > 400:
        out_file = "pearson20"
    elif int(tester_list[0].id) > 300:
        out_file = "pearson10"
    else:
        out_file = "pearson5"

    for tester in tester_list:
        if (tpc % 10) == 0:
            print("[INFO] Processed {}/{} in {}.".format(tpc, len(tester_list), out_file))
        results.append(predict.getPearsonPrediction(tester, trainer_list))
        tpc += 1
    datawrite.writePredictions(results, out_file+".txt")
    print("[INFO] Wrote results to file.")
    accept.do_check(out_file + ".txt")

def do_pearsonIUF(tester_list, trainer_list):
    pass

#FUNCTION: main
#DESCRIPTION: the main execution block for Project 2
def main():

    train_file = "./train.txt"
    test_files = ["./test5.txt", "./test10.txt", "./test20.txt"]

    #PHASE 1: Read in data from text files and convert it into python data-structures
    load_start = timeit.default_timer()

    trainers = dataload.training_data(train_file)
    testers_5 = dataload.testing_data(test_files[0])
    testers_10 = dataload.testing_data(test_files[1])
    testers_20 = dataload.testing_data(test_files[2])

    load_dur_str = "%.3f" % (timeit.default_timer() - load_start)
    print("[TIMER] Loaded Files ({} seconds)".format(load_dur_str))

    #PHASE 2: Make predictions using cosine similarity
    #CURRENT BEST OVERALL MAE:  1.0122
    #NEW COSINE SIM MAE:        1.0164
    #TOP 100:                   1.0547
    #TOP 50:                    1.0547
    #TOP 10, NEW COM_RTS:       1.0199
    cosine_start = timeit.default_timer()
    do_cosine(testers_5, trainers)
    do_cosine(testers_10, trainers)
    do_cosine(testers_20, trainers)
    cosine_dur_str = "%.3f" % (timeit.default_timer() - cosine_start)
    print("[TIMER] Made Cosine Predictions ({} seconds)".format(cosine_dur_str))
    '''
    #PHASE 3: Make predictions using pearson similarity
    #CURRENT BEST OVERALL MAE: 1.0463
    pearson_start = timeit.default_timer()
    do_pearson(testers_5, trainers)
    do_pearson(testers_10, trainers)
    do_pearson(testers_20, trainers)
    pearson_dur_str = "%.3f" % (timeit.default_timer() - pearson_start)
    print("[TIMER] Made Pearson predictions. ({} seconds)".format(pearson_dur_str))
    '''
    #PHASE 4: Make predictions for each user using a third method and output results

    print("[INFO] Nothing else to do;")
    sys.exit(0)

if __name__=="__main__":
    main()
