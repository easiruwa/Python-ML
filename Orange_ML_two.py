################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2015                        #
#                  Russell Glick '17 and Ben Sklar '18                         #
#          Machine Learning in Python with test daata - Orange                 #
#                            Orange_ML_two.py                                  #
#                                                                              #
#   This program is called in the main project and is used to generate         #
#   Machine Learning Results of the data that are analyzed by Orange           #
#                                                                              #
#   Notices: There is no main in this program. This program does not need to   #
#   be changed for different files.                                            #
#                                                                              #
#                         DON'T TOUCH THIS PROGRAM                             #
################################################################################

# Need to import these modules to run the following code.
import Orange
import csv
from Orange.classification import svm
from Orange.classification.svm import SVMLearner

# This is for Learn and Test on Test Data Accuracy
# and AUC (Area-Under-the-Curve)
# Machine Learning Algorithms are here
# Parameters are train_set and test_set (set in main proj.py file),
# and knear which is in the main proj.py file for # of Neighbors (knnk)
# Train_set is the set (multiple subjects) by which the ML tests itself on
# Test_set is the set (one-subject) by which the ML uses the train_set to 
# test on
def Orange_ML_Algorithms_learn_and_test_on_test_data(train_set,test_set,knear):
    csv_row1 = ["Accuracy:"]
    csv_row2 = ["AUC:"]

    # K Nearest Neighbors Algorithm with Learn and Test on Test Data
    # Has 0 Neighbors
    knn = Orange.classification.knn.kNNLearner()
    res = Orange.evaluation.testing.learn_and_test_on_test_data([knn],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has K number of Neighbors (you set this in the main proj.py file)
    knnk = Orange.classification.knn.kNNLearner(k=knear)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([knnk],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has 3 Neighbors
    knn3 = Orange.classification.knn.kNNLearner(k=3)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([knn3],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has 5 Neighbors
    knn5 = Orange.classification.knn.kNNLearner(k=5)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([knn5],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Nu_SVC (default) and Polynomial SVM Kernel
    svm = Orange.classification.svm.SVMLearner()
    res = Orange.evaluation.testing.learn_and_test_on_test_data([svm],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Nu_SVC (default) and Polynomial SVM Kernel
    svmp = Orange.classification.svm.SVMLearner(kernel_type=SVMLearner.
                                                Polynomial)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([svmp],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Naive Bayes Algorithm with Leave-One-Out
    bayes = Orange.classification.bayes.NaiveLearner()
    res = Orange.evaluation.testing.learn_and_test_on_test_data([bayes],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Regression Tree Learner Algorithm with Leave-One-Out
    # Max Depth is set to 5.
    tree = Orange.regression.tree.TreeLearner(max_depth = 5)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([tree],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    return csv_row1,csv_row2

# This is for Leave-One-Out Accuracy and AUC (Area-Under-the-Curve)
# Machine Learning Algorithms are here which also includes best Feature
# Selection (FS).
# Parameters are data input (set in main proj.py file),
# knear which is in the main proj.py file for # of Neighbors (knnk),
# and n is for # of best features to use (set to 100).
# Train_set is the set (multiple subjects) by which the ML tests itself on
# Test_set is the set (one-subject) by which the ML uses the train_set to 
# test on
def Orange_ML_Algorithms_learn_and_test_on_test_data_FS(train_set,test_set,
                                                        knear,n):
    csv_row1 = ["", "Accuracy:"]
    csv_row2 = ["", "AUC:"]

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has 0 Neighbors
    knn = Orange.classification.knn.kNNLearner()
    learner = Orange.feature.selection.FilteredLearner(knn,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has K number of Neighbors (you set this in the main proj.py file)
    knnk = Orange.classification.knn.kNNLearner(k=knear)
    learner = Orange.feature.selection.FilteredLearner(knnk,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has 3 Neighbors
    knn3 = Orange.classification.knn.kNNLearner(k=3)
    learner = Orange.feature.selection.FilteredLearner(knn3,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has 5 Neighbors
    knn5 = Orange.classification.knn.kNNLearner(k=5)
    learner = Orange.feature.selection.FilteredLearner(knn5,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Nu_SVC (default) and RBF kernel (default)
    svm = Orange.classification.svm.SVMLearner()
    learner = Orange.feature.selection.FilteredLearner(svm,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Nu_SVC (default) and Polynomial SVM Kernel
    svmp = Orange.classification.svm.SVMLearner(kernel_type=SVMLearner.
                                                Polynomial)
    learner = Orange.feature.selection.FilteredLearner(svmp,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Naive Bayes Algorithm with Leave-One-Out
    # Includes Feature Selection
    bayes = Orange.classification.bayes.NaiveLearner()
    learner = Orange.feature.selection.FilteredLearner(bayes,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Regression Tree Learner Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Max Depth is set to 5.
    tree = Orange.regression.tree.TreeLearner(max_depth = 5)
    learner = Orange.feature.selection.FilteredLearner(tree,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(train_set)
    res = Orange.evaluation.testing.learn_and_test_on_test_data([learner],
                                                                train_set,
                                                                test_set)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])
    return csv_row1,csv_row2

# This is the function that creates exactly how the Excel .csv file should look
def ML_Algos(train_set,test_set,csv_rows,knear,n):
    
    # For each "learn_and_test_on_test_data," do machine learning.
    row4, row5 = Orange_ML_Algorithms_learn_and_test_on_test_data(train_set,
                                                                  test_set,
                                                                  knear)
    r4,r5 = Orange_ML_Algorithms_learn_and_test_on_test_data_FS(train_set,
                                                                test_set,
                                                                knear,n/3)
    r05,r06 = Orange_ML_Algorithms_learn_and_test_on_test_data_FS(train_set,
                                                                  test_set,
                                                                  knear,n/10)
    r07,r08 = Orange_ML_Algorithms_learn_and_test_on_test_data_FS(train_set,
                                                                  test_set,
                                                                  knear,n)
    row4 += (r4+r05+r07)
    row5 += (r5+r06+r08)
    csv_rows.append(["Learn and Test on Test Data","KNN-0","KNN-K","KNN-3",
                     "KNN-5","SVM", "SVM-POLY", "NB", "TREE", ""]*4)
    csv_rows.append(row4)
    csv_rows.append(row5)
    return csv_rows

# The name of the essential main-esque function.
# Does No Feature Selection Machine Learning,
# Feature Selection N/3, Feature Selection N/10,
# Feature Selection N = (set this, set to 100 currently).
# Does for the .arff (BSP) and .tab (SAX) into one .csv Excel file.
# This is for learn and test on test data
# Need a train_set (IE: 3001-3009 = train, test on 3010)
# Need a test_set (IE: 1 subject, 3010)
def orange_two(test_set,knear,n):
    train_set1 = Orange.data.Table("All_Test_Data_No_"
                                   +test_set+"_Arff")
    train_set2 = Orange.data.Table("All_Test_Data_No_"+test_set
                                   +"_Sax_Output")
    test_set1 = Orange.data.Table(test_set+"_All_Data_Arff")
    test_set2 = Orange.data.Table(test_set+"_All_Data_Sax_Output")
        
    csv_rows = [["No Feature Selection BSP","","","","","","","","","",
                 "Feature Selection N/3 BSP", "","","","","","","","","",
                 "Feature Selection N/10 BSP","","","","","","","","","",
                 "Feature Selection N = 100 BSP"]]
    
    csv_rows = ML_Algos(train_set1,test_set1,csv_rows,knear,n)
    csv_rows.append([])
    csv_rows.append(["No Feature Selection SAX","","","","","","","","","",
                 "Feature Selection N/3 SAX", "","","","","","","","","",
                 "Feature Selection N/10 SAX","","","","","","","","","",
                 "Feature Selection N = 100 SAX"])
    
    return ML_Algos(train_set2,test_set2,csv_rows,knear,n)
