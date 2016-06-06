################################################################################
#                 HAMILTON COLLEGE SUMMER RESEARCH 2015                        #
#                  Russell Glick '17 and Ben Sklar '18                         #
#                  Machine Learning in Python - Orange                         #
#                              Orange_ML.py                                    #
#                                                                              #
#   This program is called in the main project and is used to generate         #
#   Machine Learning Results of the data that are analyzed by Orange           #
#                                                                              #
#   Notices: There is no main in this program. This program does not need to   #
#            be changed for different files.                                   #
#                                                                              #
#                         DON'T TOUCH THIS PROGRAM                             #
################################################################################

# Need to import these modules to run the following code.
import Orange
import csv
from Orange.classification import svm
from Orange.classification.svm import SVMLearner

# This is for Cross-Validation Accuracy and AUC (Area-Under-the-Curve)
# Machine Learning Algorithms are here.
# Parameters are data input (set in main proj.py file),
# header (already set) f (f for folds, set to 2, 5, and 10 already),
# and knear which is in the main proj.py file for # of Neighbors (knnk)
def Orange_ML_Algorithms(data,header,f,knear):
    csv_row1 = ["Accuracy:"]
    csv_row2 = ["AUC:"]
    # Folds are different. First fold is 2, then 5, and then 10.

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Has 0 Neighbors
    knn = Orange.classification.knn.kNNLearner()
    res = Orange.evaluation.testing.cross_validation([knn], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Has K number of Neighbors (you set this in the main proj.py file)
    knnk = Orange.classification.knn.kNNLearner(k=knear)
    res = Orange.evaluation.testing.cross_validation([knnk], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Has 3 Neighbors
    knn3 = Orange.classification.knn.kNNLearner(k=3)
    res = Orange.evaluation.testing.cross_validation([knn3], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Has 5 Neighbors
    knn5 = Orange.classification.knn.kNNLearner(k=5)
    res = Orange.evaluation.testing.cross_validation([knn5], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Cross-Validation + Number of Folds
    # Nu_SVC (default) and RBF kernel (default)
    svm = Orange.classification.svm.SVMLearner()
    res = Orange.evaluation.testing.cross_validation([svm], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Cross-Validation + Number of Folds
    # Nu_SVC (default) and Polynomial SVM Kernel
    svmp = Orange.classification.svm.SVMLearner(kernel_type=SVMLearner.
                                                Polynomial)
    res = Orange.evaluation.testing.cross_validation([svmp], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Naive Bayes Algorithm with Cross-Validation + Number of Folds
    bayes = Orange.classification.bayes.NaiveLearner()
    res = Orange.evaluation.testing.cross_validation([bayes], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Regression Tree Learner Algorithm with Cross-Validation + Number of Folds
    # Max Depth is set to 5.
    tree = Orange.regression.tree.TreeLearner(max_depth = 5)
    res = Orange.evaluation.testing.cross_validation([tree], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])
    return csv_row1,csv_row2

# This is for Cross-Validation Accuracy and AUC (Area-Under-the-Curve)
# Machine Learning Algorithms are here which also includes best Feature
# Selection (FS).
# Parameters are data input (set in main proj.py file),
# header (already set) f (f for folds, set to 2, 5, and 10 already),
# knear which is in the main proj.py file for # of Neighbors (knnk),
# and n is for # of best features to use (set to 100)
def Orange_ML_Algorithms_FS(data,header,f,knear,n):
    csv_row1 = ["", "Accuracy:"]
    csv_row2 = ["", "AUC:"]
    # Folds are different. First fold is 2, then 5, and then 10.

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Has 0 Neighbors
    knn = Orange.classification.knn.kNNLearner()
    learner = Orange.feature.selection.FilteredLearner(knn,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Has K number of Neighbors (you set this in the main proj.py file)
    knnk = Orange.classification.knn.kNNLearner(k=knear)
    learner = Orange.feature.selection.FilteredLearner(knnk,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Has 3 Neighbors
    knn3 = Orange.classification.knn.kNNLearner(k=3)
    learner = Orange.feature.selection.FilteredLearner(knn3,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Has 5 Neighbors
    knn5 = Orange.classification.knn.kNNLearner(k=5)
    learner = Orange.feature.selection.FilteredLearner(knn5,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Nu_SVC (default) and RBF kernel (default)
    svm = Orange.classification.svm.SVMLearner()
    learner = Orange.feature.selection.FilteredLearner(svm,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Nu_SVC (default) and Polynomial SVM Kernel
    svmp = Orange.classification.svm.SVMLearner(kernel_type=SVMLearner.
                                                Polynomial)
    learner = Orange.feature.selection.FilteredLearner(svmp,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Naive Bayes Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    bayes = Orange.classification.bayes.NaiveLearner()
    learner = Orange.feature.selection.FilteredLearner(bayes,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Regression Tree Learner Algorithm with Cross-Validation + Number of Folds
    # Includes Feature Selection
    # Max Depth is set to 5.
    tree = Orange.regression.tree.TreeLearner(max_depth = 5)
    learner = Orange.feature.selection.FilteredLearner(tree,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.cross_validation([learner], data, folds=f)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])
    return csv_row1,csv_row2


# This is for Cross-Validation (Leave-One-Out) Accuracy
# and AUC (Area-Under-the-Curve)
# Machine Learning Algorithms are here
# Parameters are data input (set in main proj.py file),
# and knear which is in the main proj.py file for # of Neighbors (knnk)
def Orange_ML_Algorithms_Leave_One_Out(data,knear):
    csv_row1 = ["Accuracy:"]
    csv_row2 = ["AUC:"]

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has 0 Neighbors
    knn = Orange.classification.knn.kNNLearner()
    res = Orange.evaluation.testing.leave_one_out([knn], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has K number of Neighbors (you set this in the main proj.py file)
    knnk = Orange.classification.knn.kNNLearner(k=knear)
    res = Orange.evaluation.testing.leave_one_out([knnk], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has 3 Neighbors
    knn3 = Orange.classification.knn.kNNLearner(k=3)
    res = Orange.evaluation.testing.leave_one_out([knn3], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Has 5 Neighbors
    knn5 = Orange.classification.knn.kNNLearner(k=5)
    res = Orange.evaluation.testing.leave_one_out([knn5], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Nu_SVC (default) and Polynomial SVM Kernel
    svm = Orange.classification.svm.SVMLearner()
    res = Orange.evaluation.testing.leave_one_out([svm], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Nu_SVC (default) and Polynomial SVM Kernel
    svmp = Orange.classification.svm.SVMLearner(kernel_type=SVMLearner.
                                                Polynomial)
    res = Orange.evaluation.testing.leave_one_out([svmp], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Naive Bayes Algorithm with Leave-One-Out
    bayes = Orange.classification.bayes.NaiveLearner()
    res = Orange.evaluation.testing.leave_one_out([bayes], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Regression Tree Learner Algorithm with Leave-One-Out
    # Max Depth is set to 5.
    tree = Orange.regression.tree.TreeLearner(max_depth = 5)
    res = Orange.evaluation.testing.leave_one_out([tree], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    return csv_row1,csv_row2

# This is for Leave-One-Out Accuracy and AUC (Area-Under-the-Curve)
# Machine Learning Algorithms are here which also includes best Feature
# Selection (FS).
# Parameters are data input (set in main proj.py file),
# knear which is in the main proj.py file for # of Neighbors (knnk),
# and n is for # of best features to use (set to 100).
def Orange_ML_Algorithms_Leave_One_Out_FS(data,knear,n):
    csv_row1 = ["", "Accuracy:"]
    csv_row2 = ["", "AUC:"]

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has 0 Neighbors
    knn = Orange.classification.knn.kNNLearner()
    learner = Orange.feature.selection.FilteredLearner(knn,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has K number of Neighbors (you set this in the main proj.py file)
    knnk = Orange.classification.knn.kNNLearner(k=knear)
    learner = Orange.feature.selection.FilteredLearner(knnk,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has 3 Neighbors
    knn3 = Orange.classification.knn.kNNLearner(k=3)
    learner = Orange.feature.selection.FilteredLearner(knn3,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # K Nearest Neighbors Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Has 5 Neighbors
    knn5 = Orange.classification.knn.kNNLearner(k=5)
    learner = Orange.feature.selection.FilteredLearner(knn5,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Nu_SVC (default) and RBF kernel (default)
    svm = Orange.classification.svm.SVMLearner()
    learner = Orange.feature.selection.FilteredLearner(svm,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Support Vector Machine Algorithm with Leave-One-Out
    # Nu_SVC (default) and Polynomial SVM Kernel
    svmp = Orange.classification.svm.SVMLearner(kernel_type=SVMLearner.
                                                Polynomial)
    learner = Orange.feature.selection.FilteredLearner(svmp,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Naive Bayes Algorithm with Leave-One-Out
    # Includes Feature Selection
    bayes = Orange.classification.bayes.NaiveLearner()
    learner = Orange.feature.selection.FilteredLearner(bayes,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])

    # Regression Tree Learner Algorithm with Leave-One-Out
    # Includes Feature Selection
    # Max Depth is set to 5.
    tree = Orange.regression.tree.TreeLearner(max_depth = 5)
    learner = Orange.feature.selection.FilteredLearner(tree,
        filter=Orange.feature.selection.FilterBestN(n=n), name='filtered')
    classifier = learner(data)
    res = Orange.evaluation.testing.leave_one_out([learner], data)
    csv_row1.append("%.2f" % Orange.evaluation.scoring.CA(res)[0])
    csv_row2.append("%.2f" % Orange.evaluation.scoring.AUC(res)[0])
    return csv_row1,csv_row2

# This is the function that creates exactly how the Excel .csv file should look
def ML_Algos(data,csv_rows,knear,n):
    # Number of Folds
    headers = ["2 FOLD:","5 FOLD:","10 FOLD:"]
    folds = [2,5,10]
    # For each fold, do machine learning cross-validation
    for i in range(len(headers)):
        row1,row2 = Orange_ML_Algorithms(data,headers[i],folds[i],knear)
        r1,r2 = Orange_ML_Algorithms_FS(data,headers[i],folds[i],knear,n/3)
        r01,r02 = Orange_ML_Algorithms_FS(data,headers[i],folds[i],knear,n/10)
        r03,r04 = Orange_ML_Algorithms_FS(data,headers[i],folds[i],knear,n)
        row1 += (r1+r01+r03)
        row2 += (r2+r02+r04)
        csv_rows.append([headers[i],"KNN-0","KNN-K","KNN-3","KNN-5",
                         "SVM", "SVM-POLY", "NB", "TREE", ""]*4)
        csv_rows.append(row1)
        csv_rows.append(row2)
        csv_rows.append([])

    # For each "Leave-One-Out" do machine learning.
    row4, row5 = Orange_ML_Algorithms_Leave_One_Out(data,knear)
    r4,r5 = Orange_ML_Algorithms_Leave_One_Out_FS(data,knear,n/3)
    r05,r06 = Orange_ML_Algorithms_Leave_One_Out_FS(data,knear,n/10)
    r07,r08 = Orange_ML_Algorithms_Leave_One_Out_FS(data,knear,n)
    row4 += (r4+r05+r07)
    row5 += (r5+r06+r08)
    csv_rows.append(["Leave One Out","KNN-0","KNN-K","KNN-3","KNN-5",
                         "SVM", "SVM-POLY", "NB", "TREE", ""]*4)
    csv_rows.append(row4)
    csv_rows.append(row5)
    return csv_rows

# The name of the essential main-esque function.
# Does No Feature Selection Machine Learning,
# Feature Selection N/3, Feature Selection N/10,
# Feature Selection N = (set this, set to 100 currently).
# Does for the .arff (BSP) and .tab (SAX) into one .csv Excel file.
def orange(data,knear,n):
    data1 = Orange.data.Table((data+"_Arff"))
    data2 = Orange.data.Table((data+"_Sax_Output"))  
    csv_rows = [["No Feature Selection BSP","","","","","","","","","",
                 "Feature Selection N/3 BSP", "","","","","","","","","",
                 "Feature Selection N/10 BSP","","","","","","","","","",
                 "Feature Selection N = 100 BSP"]]
    
    csv_rows = ML_Algos(data1,csv_rows,knear,n)
    csv_rows.append([])
    csv_rows.append(["No Feature Selection SAX","","","","","","","","","",
                 "Feature Selection N/3 SAX", "","","","","","","","","",
                 "Feature Selection N/10 SAX","","","","","","","","","",
                 "Feature Selection N = 100 SAX"])
    
    return ML_Algos(data2,csv_rows,knear,n)
