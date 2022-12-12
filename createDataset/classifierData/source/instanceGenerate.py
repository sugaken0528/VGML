# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import MeCab
from lowerWord import LowerWord
# from wordTree_en import treeGraph_en
from calcConceptLebel import CalcConceptLevel


class instanceGenerate:
    def __init__(self):
        pass

    def doins(self, necessaryList, classList):
        m = MeCab.Tagger("-Ochasen")
        # クラスの候補となる単語に接続する単語を抽出
        instanceList = []
        otherList = []
        for i in range(len(classList)):
            classifierList = []
            connectWordList = []
            classWord = classList[i]
            classifierList.append([classWord])
            classConceptLevel = self.calcAverageConceptLevel(
                m.parse(classWord).splitlines(), True)
            for j in range(len(necessaryList)):
                # classWordが前または後ろに接続する単語を抽出
                if necessaryList[j][0].startswith(classWord) and necessaryList[j][0] != classWord and self.largerConceptLevel(classConceptLevel, necessaryList[j][0]) == True:
                    connectWordList.append(necessaryList[j][0])
                elif necessaryList[j][0].startswith(classWord) and necessaryList[j][0] != classWord and self.largerConceptLevel(classConceptLevel, necessaryList[j][0]) == False:
                    otherList.append([necessaryList[j][0]])
            classifierList.append([connectWordList])
            classifierList = self.removeDuplicateInstance(
                classList, classifierList)
            instanceList.append(classifierList)

        # クラスとインスタンス候補となる単語以外を抽出
        for wordId in range(len(necessaryList)):
            count = 0
            for classId in range(len(instanceList)):
                # クラスと一致する単語の場合
                if necessaryList[wordId][0] == instanceList[classId][0][0]:
                    count += 1
                # クラスがインスタンス変数を持つ場合
                if len(instanceList[classId]) >= 2:
                    for instanceId in range(len(instanceList[classId][1])):
                        # インスタンス変数と一致する単語の場合
                        if necessaryList[wordId][0] == instanceList[classId][1][instanceId]:
                            count += 1
            if count == 0:
                otherList.append(necessaryList[wordId])
        return instanceList, otherList

    def largerConceptLevel(self, classConceptLevel, instanceWord):
        m = MeCab.Tagger("-Ochasen")
        instanceNouns = m.parse(instanceWord).splitlines()
        instanceConceptLevel = self.calcAverageConceptLevel(
            instanceNouns, False)

        if classConceptLevel < 10:
            classConceptLevel = 10

        if classConceptLevel + 5 >= instanceConceptLevel:
            return True
        else:
            return False

    def calcAverageConceptLevel(self, nouns, classFlag):
        # インスタンス変数の場合クラスに接続する名詞のみを考える
        if classFlag == False and len(nouns) >= 3:
            nouns = nouns[1:]
        conceptLevel = 0
        for i in range(len(nouns)-1):
            # 上位概念の辞書と同義語のリストを取得
            lowerWord = LowerWord()
            dict, semiList = lowerWord.SearchTopConceptWords(
                nouns[i].split()[0])
            if dict != 0 and semiList != 0:
                calcConceptLebel = CalcConceptLevel(dict, semiList)
                conceptLevel += calcConceptLebel.calc()
        return conceptLevel / (len(nouns)-1)

    # 重複するインスタンスを削除
    def removeDuplicateInstance(self, classList, classifierList):
        """
        classifierList: [[クラス],[instance1,instance2, ・・・]]
        classList: [クラス1, クラス2, ・・・]
        """
        removeList = []  # 削除するインスタンスを格納
        # 他のクラスと重複するインスタンスを抽出
        for i in range(len(classList)):
            duplicateWord = ""
            for j in range(len(classifierList[1][0])):
                # インスタンス変数がいずれかのクラスと一致する場合
                if classList[i] != classifierList[0][0] and classList[i] == classifierList[1][0][j]:
                    removeList.append(classifierList[1][0][j])
                    removeList.append(classList[i])
                    # print("{}と{}".format(
                    # classList[i], classifierList[1][0][j]))
                    duplicateWord = classifierList[1][0][j]
                    # print("{}と{}が等しいのでduplicateWordを{}とします".format(
                    # classList[i], classifierList[1][0][j], duplicateWord))
                if duplicateWord != classifierList[1][0][j] and duplicateWord in classifierList[1][0][j] and duplicateWord != "":
                    # print("{}は{}を含むので追加します".format(
                    # classifierList[1][0][j], duplicateWord))
                    removeList.append(classifierList[1][0][j])

        classInstanceList = []  # クラスと他のクラスと重複したインスタンス変数を除いたセットを格納
        classInstanceList.append(classifierList[0])
        instanceList = []
        for i in range(len(classifierList[1][0])):
            if classifierList[1][0][i] not in removeList:
                instanceList.append(classifierList[1][0][i])
        classInstanceList.append(instanceList)
        return classInstanceList
