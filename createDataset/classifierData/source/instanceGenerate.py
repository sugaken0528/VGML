# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
from lowerWord import LowerWord
#from wordTree_en import treeGraph_en
from calcConceptLebel import CalcConceptLevel


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

        # 重複を削除
        tempList = []
        for x in classifierList:
            if x in classDataList:
                pass
            else:
                tempList.append(x)
        classifierList = tempList

        # print("\n")
        # print(classDataList)
        # print("\n")

        compareList = []  # インスタンス変数候補をクラスごとに格納
        classFlag = 0
        new_classList = []  # インスタンス変数候補を持つクラスを格納
        for x in classDataList:
            conInsList = []
            for y in classifierList:
                if x in y:
                    conInsList.append(y)
                    classFlag = 1
            if classFlag == 1:
                new_classList.append(x)
            if conInsList != []:
                compareList.append(conInsList)
            classFlag = 0

        # print(new_classList)
        print("\n")
        # print(compareList)
        self.extractInstance(new_classList, compareList)

    # インスタンスを抽出
    def extractInstance(self, classList, compareList):
        instansList = []
        for i in range(len(classList)):
            tempList = []
            target = classList[i]
            for j in range(len(compareList[i])):
                str = compareList[i][j]
                idx = str.find(target)
                back = str[idx+len(target):]
                front = str[:idx]
                flag = 0
                for x in classList:
                    if x in front or x in back:
                        flag = 1
                if back != '' and front != '':
                    pass
                elif back == '' and front != '' and flag == 0:
                    tempList.append(front)
                elif back != '' and front == '' and flag == 0:
                    tempList.append(back)
            instansList.append(tempList)
        print(classList)
        print(instansList)

        for i in range(len(classList)):
            for j in range(len(instansList[i])):
                lowerWord = LowerWord()
                dict, semiList = lowerWord.SearchTopConceptWords(
                    instansList[i][j])
                if dict != 0 and semiList != 0:
                    calcConceptLebel = CalcConceptLevel(dict, semiList)
                    calc = calcConceptLebel.calc()
                    print("{} : {}".format(instansList[i][j], calc))


"""
target = 'time: '
idx = s.find(target)
r = s[idx+len(target):]
"""
