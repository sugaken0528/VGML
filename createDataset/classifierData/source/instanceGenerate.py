import pandas as pd
import numpy as np
import csv


class instanceGenerate:
    def __init__(self):
        pass

    def doins(self):
        classifier = pd.read_csv(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_intern.csv")
        classData = pd.read_csv(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_intern_class.csv")

        classifierList = []  # 分類単語格納リスト
        classDataList = []  # クラス候補格納リスト

        classifierList.append(classifier.columns[1])
        classDataList.append(classData.columns[0])

        for x in classifier.values:
            classifierList.append(x[1])

        for x in classData.values:
            classDataList.append(x[0])

        print("\n")
        print(classDataList)
        print("\n")
        print(classifierList)
