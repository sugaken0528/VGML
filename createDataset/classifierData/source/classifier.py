# クラスとインスタンス変数、その他で分類するクラス
import pandas as pd
import numpy as np
import csv
import MeCab
import os


class classifier:
    def __init__(self, result, docs1, docs, wlist1, TF_list):
        self.result = result
        self.docs1 = docs1
        self.docs = docs
        self.wlist1 = wlist1
        self.TF_list = TF_list

    def createClassifierList(self):
        wordList = []
        classList = []
        for x in self.result.values:
            if x[10] >= 1.0:
                list_ = []
                list_.append("INDEX_ID")
                list_.append(x[0])
                wordList.append(list_)
            if x[9] >= 0.11:
                classList.append(x[0])

        # 重複の削除およびソート
        wordList.sort()
        classList.sort()
        wordList = self.get_unique_list(wordList)
        classList = self.get_unique_list(classList)

        dic = pd.read_csv(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\dic.csv")
        counter_suffix = ['位', '宇', '折', '果', '箇', '荷', '菓', '掛', '顆', '回', '階', '画', '頭', '方', '株', '巻', '管', '缶', '基', '機', '騎', '切', '客', '脚', '行', '局', '句', '軀', '口', '具', '組', '景', '桁', '件', '軒', '個', '戸', '号', '合', '梱', '献', '喉', '座', '棹', '冊', '皿', '氏', '締', '字', '軸', '室', '首', '重', '床', '条', '畳', '錠', '帖', '筋', '食', '隻', '膳', '双',
                          '艘', '足', '揃', '体', '袋', '台', '題', '立', '卓', '束', '玉', '着', '丁', '挺', '帳', '張', 'つ', '対', '通', '番', '粒', '艇', '滴', '点', '度', '等', '堂', '人', '把', '羽', '張', '刎', '杯', '柱', '鉢', '発', '尾', '匹', '瓶', '振', '部', '幅', '服', '房', '篇', '遍', '本', '間', '枚', '前', '幕', '棟', '名', '面', '門', '問', '山', '葉', '流', '旒', '両', '領', '輪', '連', '椀', '碗']
        v_list = []

        value = ""
        for x in self.docs1:
            for y in x.split():
                if (any(map(str.isdigit, y))):  # 数字を含む文章かどうか
                    for num in y:
                        if num.isdigit() or num == ".":
                            value = value+num
                    for z in counter_suffix:
                        if not len(y) == y.find(value)+len(value):
                            if z in y[y.find(value)+len(value)]:  # 文章中に単位があるか
                                for d in dic.values:
                                    if not (d[2] is np.nan):
                                        if z in d[2]:
                                            for y2 in x.split():
                                                # 単位がある文にその単位を使う名詞があるか
                                                if d[1] in y2 and not y2[len(y2)-1].isdigit() and not y == y2:
                                                    list_ = []
                                                    list_.append("INDEX_ID")
                                                    list_.append(y2)
                                                    list_.append(value)
                                                    v_list.append(list_)
                value = ""
        d_list = []
        for x in v_list:
            for count_w, y in enumerate(self.wlist1):
                if y == x[1]:  # 定数名の単語を探す
                    for p, z in enumerate(self.TF_list):
                        if z[count_w] > 0:  # 定数名のTF_IDF値を持つ文を抽出
                            sentence_list = []
                            for count_TF, l in enumerate(z):
                                if l > 0:
                                    sentence_list.append(self.wlist1[count_TF])
                                lists_ = []
                                lists_.append(x[1])
                                lists_.append(x[2])
                                lists_.append(z[count_w])
                                for m in sentence_list:
                                    for d in counter_suffix:
                                        if x[2] in m and d in m:
                                            d_list.append(lists_)
        d_list = self.get_unique_list(d_list)
        d_list.sort()
        d_list
        f_list = []
        tmp = ["", 0, 0]
        for x in d_list:
            if tmp[0] == "" or not tmp[0] == x[0]:
                f_list.append(tmp)
                tmp = x
            if tmp[2] < x[2]:
                tmp = x
        f_list.append(tmp)
        f_list.pop(0)
        f_list
        for x in f_list:
            list_ = []
            list_.append("INDEX_ID")
            list_.append(x[0])
            list_.append(x[1])
            wordList.append(list_)
        new_list = sorted(wordList, reverse=True)

        # クラスの候補となる単語に接続する単語を抽出
        instanceList = []
        for i in range(len(classList)):
            classifierList = []
            classWord = classList[i]
            classifierList.append([classWord])
            for j in range(len(wordList)):
                # classWordが前または後ろに接続する単語を抽出
                if (wordList[j][1].startswith(classWord) and wordList[j][1] != classWord):
                    classifierList.append(wordList[j])
            classifierList = self.removeDuplicateInstance(
                classList, classifierList)
            instanceList.append(classifierList)

        # インスタンス候補となる単語以外を抽出
        otherList = []
        for i in range(len(wordList)):
            count = 0
            for j in range(len(instanceList)):
                for k in range(len(instanceList[j]) - 1):
                    if wordList[i][1] == instanceList[j][k+1][1]:
                        count += 1
                for k in range(len(instanceList[j])):
                    if wordList[i][1] == instanceList[j][k][0]:
                        count += 1
            if count == 0:
                otherList.append(wordList[i])

        os.makedirs(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance", exist_ok=True)
        # クラスとインスタンス変数の書き込み
        for i in range(len(instanceList)):
            classWord = classList[i]
            print(classWord)
            for x in instanceList[i]:
                with open("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance\\"+classWord+".csv", 'w', encoding='utf8') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    for x in instanceList[i]:
                        writer.writerow(x)

        # その他を書き込み
        with open("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance\\advance.csv", 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            for x in otherList:
                writer.writerow(x)

    # 重複の削除およびソート
    def get_unique_list(self, seq):
        seen = []
        return [x for x in seq if x not in seen and not seen.append(x)]

    # 重複するインスタンスを削除
    def removeDuplicateInstance(self, classList, classifierList):
        tempList = []
        # print(classifierList)
        removeList = []
        # 重複するインスタンスを抽出
        for i in range(len(classList)):
            duplicateWord = ""
            for j in range(len(classifierList)-1):
                if classList[i] != classifierList[0][0] and classList[i] == classifierList[j+1][1]:
                    removeList.append(classifierList[0][0])
                    removeList.append(classList[i])
                    # print("{}と{}".format(classList[i], classifierList[0][0]))
                    duplicateWord = classifierList[j+1][1]
                    # print("{}と{}が等しいのでduplicateWordを{}とします".format(
                    # classList[i], classifierList[j+1][1], duplicateWord))
                if duplicateWord != classifierList[j+1][1] and duplicateWord in classifierList[j+1][1] and duplicateWord != "":
                    # print("{}は{}を含むので追加します".format(
                    # classifierList[j+1][1], duplicateWord))
                    removeList.append(classifierList[j+1][1])

        # 重複するインスタンスを削除
        tempList = []
        tempList.append([classifierList[0][0]])
        for i in range(len(classifierList)-1):
            if classifierList[i+1][1] not in removeList[1:]:
                tempList.append(classifierList[i+1])
        return tempList


"""
    # リスト内の品詞を取得する
     m = MeCab.Tagger("-Ochasen")
        for x in new_list:
            nouns = m.parse(x[1]).splitlines()
            for i in range(len(nouns)):
                print(nouns[i].split())
            print('-----------------------------------')

  # クラスをcsvファイルに書き込む
  new_classList = []
   for i in range(len(classList)):
        tempList = [classList[i]]
        new_classList.append(tempList)
    new_classList = sorted(new_classList, reverse=True)
    with open("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance_class.csv", 'w', encoding='utf8') as f:
        writer = csv.writer(f, lineterminator='\n')
        for x in new_classList:
            writer.writerow(x)
"""
