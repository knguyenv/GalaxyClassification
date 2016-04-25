import numpy as np
import glob
from PIL import Image
import math

import pylab as pl
import skimage.io as io
import matplotlib.pyplot as plt

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.cross_validation import KFold


#Calculate the Root Mean Square Percentage Error
def CalculateScore(y_real, y_predict):
    score = 0
    for i in range (0, len(y_real)):
        real = y_real[i]
        predict = y_predict[i]
        if real == predict: score += 1
    score = score * 1.0 / len(y_real)
    return score


#Build data model from sample set. Mode=2 use SVM, otherwise use Random Forest
def BuildDataModel(samples, labels, mode):
    dataSet = np.array(samples)
    labelsSet = np.array(labels)

    if mode == 2:
        #clf = SVC(1.0, kernel='linear')   #Use default rbf kernel
        clf = AdaBoostClassifier(SVC(probability=True, kernel='linear'), n_estimators = 5)
    else:
        #clf = RandomForestClassifier(n_estimators=200)
        clf = ExtraTreesClassifier(n_estimators=4000, max_depth=None, min_samples_split=1, random_state=0, max_features = 400)
    score = 0

    kf = KFold(len(samples), n_folds=10)
    sklearn.cross_validation.KFold(n=len(samples), n_folds=10, shuffle=True, random_state=None)
    for train_index, test_index in kf:
        X_train, X_test = dataSet[train_index], dataSet[test_index]
        y_train, y_test = labelsSet[train_index], labelsSet[test_index]
        clf.fit(X_train, y_train)
        score += CalculateScore(clf.predict(X_test), y_test)
    score = score / 10
    print score


def readImageFiles(folder, type):
    imgList = []
    typeList = []

    for fName in glob.glob(folder + '*.jpeg'):
        imageArr = Image.open(fName)
        #imageArr.show()
        imageArr = np.array(imageArr)
        #imageArr[imageArr == False] = 0
        #imageArr[imageArr == True] = 255

        #showImg = Image.fromarray(imageArr, mode='1')
        #showImg.show()

        #imageArr = io.imread(fName)
        #pl.imshow(imageArr, cmap=plt.cm.Greys_r)
        #pl.imshow(imageArr, cmap='Greys',  interpolation='nearest')
        #pl.show()

        features = imageArr.flatten()
        imgList.append(features)
        typeList.append(type)

    return imgList, typeList

samples, labels = readImageFiles('2/', 2)
S2, L2 = readImageFiles('5/', 5)
samples.extend(S2)
labels.extend(L2)

#S2, L2 = readImageFiles('inputS/', 0)
#samples.extend(S2)
#labels.extend(L2)

print 'Accuracy for 2 Arms galaxy vs. 5 Arms Galaxy'
#print 'Accuracy for Smooth galaxy vs. Galaxy with arms'
BuildDataModel(samples, labels, 0)
print len(labels)