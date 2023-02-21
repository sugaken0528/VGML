import MeCab
import pandas as pd
import numpy as np


class methodGenerate:
    def __init__(self):
        pass

    def doins(self, classList, necessaryList, specName):
        m = MeCab.Tagger("-Ochasen")
        verbList = []  # 動詞化できる名詞を格納
        otherList = []  # 動詞化できる名詞以外を格納
        df = pd.read_csv("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\loadTxt\\"+specName+"_load.txt")
        # 抽出データを文ごとにarrayに格納
        docs = np.array([])
        docs = np.append(docs, df.columns)
        for x in df.values:
            docs = np.append(docs, x)

        sahen = "名詞-サ変接続"
        for wordId in range(len(necessaryList)):
            if len(necessaryList[wordId][0]) >=3:
                nouns = m.parse(necessaryList[wordId][0]).splitlines()
                partOfSpeech = nouns[-2].split()[-1]
                if partOfSpeech == sahen:
                    verbList.append(necessaryList[wordId])
                else:
                    otherList.append(necessaryList[wordId])

        classVerbList = []
        for i in range(len(verbList)):
            classVerbList = self.verbSearch(classVerbList, docs, classList, verbList[i])
        # クラスとメソッドが重複するセットを削除
        operateList = self.duplicateSet(classVerbList)

        return operateList,otherList
    
    def verbSearch(self, classVerbList, docs, classList, verb):
        for i in range(len(docs)):
            splitDocs = docs[i].split()
            classWord = self.exitClassWord(splitDocs,classList)
            if classWord == None:
                classWord = self.exitClassWord(docs[i-1].split(),classList)
            for j in range(len(splitDocs)):
                if verb[0] == splitDocs[j] and classWord != None:
                    classVerbList.append([classWord, verb[0]])
        return classVerbList

    def exitClassWord(self, splitDocs, classList):
        for i in range(len(classList)):
            classWord = classList[i]
            if classWord in splitDocs:
                return classWord
        return None

    def duplicateSet(self, classVerbList):
        tempList = []
        for i in range(len(classVerbList)):
            classVerbSet = classVerbList[i]
            if not classVerbSet in tempList:
                tempList.append(classVerbSet)
        return tempList


                    


