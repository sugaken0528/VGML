# クラスとインスタンス変数、その他で分類するクラス
import pandas as pd
import numpy as np
import csv
import MeCab
import os
import shutil


class classifier:
    def __init__(self, result, specification, wordList, TF_list):
        self.result = result
        self.specification = specification
        self.wordList = wordList
        self.TF_list = TF_list

    def createClassifierList(self):
        necessaryList = []  # VDM++仕様書に必要な候補の単語を格納
        classList = []  # クラスの候補となる単語を格納
        for x in self.result.values:
            if x[10] >= 1.0:
                necessaryList.append([x[0]])
            if x[9] >= 0.11:
                classList.append(x[0])

        # 重複の削除およびソート
        necessaryList.sort()
        classList.sort()
        necessaryList = self.get_unique_list(necessaryList)
        classList = self.get_unique_list(classList)

        how_to_count_dic = pd.read_csv(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\how_to_count_dic.csv")
        unit_dic = ['位', '宇', '折', '果', '箇', '荷', '菓', '掛', '顆', '回', '階', '画', '頭', '方', '株', '巻', '管', '缶', '基', '機', '騎', '切', '客', '脚', '行', '局', '句', '軀', '口', '具', '組', '景', '桁', '件', '軒', '個', '戸', '号', '合', '梱', '献', '喉', '座', '棹', '冊', '皿', '氏', '締', '字', '軸', '室', '首', '重', '床', '条', '畳', '錠', '帖', '筋', '食', '隻', '膳', '双',
                    '艘', '足', '揃', '体', '袋', '台', '題', '立', '卓', '束', '玉', '着', '丁', '挺', '帳', '張', 'つ', '対', '通', '番', '粒', '艇', '滴', '点', '度', '等', '堂', '人', '把', '羽', '張', '刎', '杯', '柱', '鉢', '発', '尾', '匹', '瓶', '振', '部', '幅', '服', '房', '篇', '遍', '本', '間', '枚', '前', '幕', '棟', '名', '面', '門', '問', '山', '葉', '流', '旒', '両', '領', '輪', '連', '椀', '碗']
        for sentence in self.specification:
            for word in sentence.split():
                value = ""
                if (any(map(str.isdigit, word))):  # 数字を含む単語かどうか
                    for num in word:
                        if num.isdigit() or num == ".":
                            value = value+num
                    for unit in unit_dic:
                        nextIndexValue = word.find(
                            value)+len(value)  # 単語の内数字の次の要素のインデックス
                        # 数字の次の要素に単位があるか
                        if len(word) > nextIndexValue and unit in word[nextIndexValue]:
                            for wordCountSet in how_to_count_dic.values:
                                # 数え方の辞書に単位が含まれている場合
                                if not (wordCountSet[2] is np.nan) and unit in wordCountSet[2]:
                                    for word2 in sentence.split():
                                        # 単位がある文にその単位を使う名詞があるか
                                        if wordCountSet[1] in word2 and not word2[len(word2)-1].isdigit() and not word == word2 and self.examine_include_word(word2, necessaryList):
                                            necessaryList = self.replaceWord(
                                                word2, value, necessaryList)

        # クラスの候補となる単語に接続する単語を抽出
        instanceList = []
        for i in range(len(classList)):
            classifierList = []
            connectWordList = []
            classWord = classList[i]
            classifierList.append([classWord])
            for j in range(len(necessaryList)):
                # classWordが前または後ろに接続する単語を抽出
                if (necessaryList[j][0].startswith(classWord) and necessaryList[j][0] != classWord):
                    connectWordList.append(necessaryList[j][0])
            classifierList.append([connectWordList])
            classifierList = self.removeDuplicateInstance(
                classList, classifierList)
            instanceList.append(classifierList)

        # クラスとインスタンス候補となる単語以外を抽出
        otherList = []
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

        # フォルダにアクセス権限を与え一旦削除
        os.chmod("../data/classifier_advance", 755)
        shutil.rmtree(
            "../data/classifier_advance")

        os.makedirs(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance", exist_ok=True)
        # クラスとインスタンス変数の書き込み
        for i in range(len(instanceList)):
            classWord = classList[i]
            with open("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance\\"+classWord+".csv", 'w', encoding='utf8') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow([classWord])
                for j in range(len(instanceList[i][1])):
                    writer.writerow([instanceList[i][1][j]])

        # その他を書き込み
        with open("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance\\advance.csv", 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            for x in otherList:
                writer.writerow(x)

    # 重複の削除およびソート
    def get_unique_list(self, seq):
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]

    # リスト内に指定した単語と一致する単語があるかの判定
    def examine_include_word(self, word, wordList):
        for i in range(len(wordList)):
            if wordList[i][0] == word:
                return True

    def replaceWord(self, word, value, wordList):
        for i in range(len(wordList)):
            if (wordList[i][0] == word) and len(wordList[i]) != 2:
                wordList[i] = [word, value]
        return wordList

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


"""
    # リスト内の品詞を取得する
     m = MeCab.Tagger("-Ochasen")
        for x in new_list:
            nouns = m.parse(x[1]).splitlines()
            for i in range(len(nouns)):
                print(nouns[i].split())
            print('-----------------------------------')
"""
