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
        classConnectList = []
        otherList = []
        for i in range(len(classList)):
            connectWordList = []
            classConnectSet = []
            classWord = classList[i]
            classConnectSet.append([classWord])
            for j in range(len(necessaryList)):
                # classWordを含む単語を抽出
                if necessaryList[j][0] != classWord and classWord in necessaryList[j][0]:
                    connectWordList.append(necessaryList[j][0])
            classConnectSet.append([connectWordList])
            classConnectSet = self.removeDuplicateInstance(
                classList, classConnectSet)
            classConnectList.append(classConnectSet)
        print(classConnectList)

        # クラスの概念レベルより小さい概念レベルを持つインスタンス変数を抽出
        classInstanceList = []
        for classId in range(len(classConnectList)):
            classInstanceSet = []
            classWord = classConnectList[classId][0][0]
            print(classWord)
            classInstanceSet.append([classWord])
            classConceptLevel = self.calcAverageConceptLevel(
                m.parse(classWord).splitlines(), True)
            instanceList = []
            for instanceId in range(len(classConnectList[classId][1])):
                instanceWord = classConnectList[classId][1][instanceId]
                if self.largerConceptLevel(classWord, classConceptLevel, instanceWord) == True:
                    if any(map(str.isdigit, instanceWord)) and self.numCheck(instanceWord)==False:
                        pass
                    elif self.directCheck(instanceWord) or (self.numCheck(instanceWord)==False and not any(map(str.isdigit, instanceWord))):
                        instanceList.append(
                            classConnectList[classId][1][instanceId])
                    elif self.numCheck(instanceWord)==False and any(map(str.isdigit, instanceWord)):
                        print(instanceWord)
            classInstanceSet.append(instanceList)
            classInstanceList.append(classInstanceSet)

        # クラスとインスタンス候補となる単語以外を抽出
        for wordId in range(len(necessaryList)):
            count = 0
            for classId in range(len(classInstanceList)):
                # クラスと一致する単語の場合
                if necessaryList[wordId][0] == classInstanceList[classId][0][0]:
                    count += 1
                # クラスがインスタンス変数を持つ場合
                if len(classInstanceList[classId]) >= 2:
                    for instanceId in range(len(classInstanceList[classId][1])):
                        # インスタンス変数と一致する単語の場合
                        if necessaryList[wordId][0] == classInstanceList[classId][1][instanceId]:
                            count += 1
            if count == 0:
                if self.directCheck(necessaryList[wordId][0]) == True:
                    otherList.append(necessaryList[wordId])
        return classInstanceList, otherList

    def largerConceptLevel(self, classWord, classConceptLevel, instanceWord):
        m = MeCab.Tagger("-Ochasen")
        instanceNouns = m.parse(instanceWord.replace(classWord, '')).splitlines()
        instanceConceptLevel = self.calcAverageConceptLevel(
            instanceNouns, False)
        print("クラス「{}」:{}".format(classWord,classConceptLevel))
        print("インスタンス「{}」:{}".format(instanceNouns,instanceConceptLevel))

        if classConceptLevel < 10:
            classConceptLevel = 10

        if classConceptLevel + 5 >= instanceConceptLevel:
            return True
        else:
            return False

    def calcAverageConceptLevel(self, nouns, classFlag):
        # インスタンス変数の場合クラスに接続する名詞のみを考える
        conceptLevel = 0
        for i in range(len(nouns)-1):
            # 上位概念の辞書と同義語のリストを取得
            lowerWord = LowerWord()
            dict, semiList = lowerWord.SearchTopConceptWords(
                nouns[i].split()[0])
            if dict != 0 and semiList != 0:
                calcConceptLebel = CalcConceptLevel(dict, semiList)
                conceptLevel += calcConceptLebel.doCalc()
        return conceptLevel / (len(nouns)-1)

    # 重複するインスタンスを削除
    def removeDuplicateInstance(self, classList, classConnectSet):
        """
        classConnectSet: [[クラス],[connect1,connect2, ・・・]]
        classList: [クラス1, クラス2, ・・・]
        """
        removeList = []  # 削除するインスタンスを格納
        # 他のクラスと重複するインスタンスを抽出
        for i in range(len(classList)):
            duplicateWord = ""
            for j in range(len(classConnectSet[1][0])):
                # インスタンス変数がいずれかのクラスと一致する場合
                if classList[i] != classConnectSet[0][0] and classList[i] in classConnectSet[1][0][j] and not classList[i] in classConnectSet[0][0]:
                    removeList.append(classConnectSet[1][0][j])
                    removeList.append(classList[i])
                    #print("{}と{}は等しくない".format(
                    #classList[i], classConnectSet[0][0]))
                    #print("{}と{}".format(
                    #classList[i], classConnectSet[1][0][j]))
                    duplicateWord = classConnectSet[1][0][j]
                    #print("{}と{}が等しいのでduplicateWordを{}とします".format(
                    #classList[i], classConnectSet[1][0][j], duplicateWord))
                if duplicateWord != classConnectSet[1][0][j] and duplicateWord in classConnectSet[1][0][j] and duplicateWord != "":
                    #print("{}は{}を含むので追加します".format(
                    #classConnectSet[1][0][j], duplicateWord))
                    removeList.append(classConnectSet[1][0][j])

        newClassConnectSet = []  # クラスと他のクラスと重複した接続単語を除いたセットを格納
        newClassConnectSet.append(classConnectSet[0])
        instanceList = []
        for i in range(len(classConnectSet[1][0])):
            if classConnectSet[1][0][i] not in removeList:
                instanceList.append(classConnectSet[1][0][i])
        newClassConnectSet.append(instanceList)
        return newClassConnectSet

    def directCheck(self,word):
        count = 0
        directDict = ['右','左','下','上','東','西','南','北','内','外','前','後','例','図','中心','方向']
        for i in range(len(directDict)):
            if directDict[i] in word:
                count += 1
        if count >= 1:
            return False
        else:
            return True
        
    def numCheck(self,word):
        count = 0
        directDict = ['図','表','番号','式','個']
        for i in range(len(directDict)):
            if directDict[i] in word:
                count += 1
        if count >= 1:
            return False
        else:
            return True