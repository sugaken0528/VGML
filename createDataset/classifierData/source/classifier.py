# クラスとインスタンス変数、その他で分類するクラス
import pandas as pd
import numpy as np
import csv
import os
import shutil
from instanceGenerate import instanceGenerate
from methodGenerate import methodGenerate
from vdmGenerate import vdmGenerate


class classifier:
    def __init__(self, specName, result, specification, wordList, TF_list):
        self.specName = specName
        self.result = result
        self.specification = specification
        self.wordList = wordList
        self.TF_list = TF_list
        self.instanceGenerate = instanceGenerate()
        self.methodGenerate = methodGenerate()
        self.vdmGenerate = vdmGenerate(self.specName)

    def createClassifierList(self):
        necessaryList = []  # VDM++仕様書に必要な候補の単語を格納
        classList = []  # クラスの候補となる単語を格納
        for x in self.result.values:
            if x[10] == 1.0:
                necessaryList.append([x[0]])
            #if x[10] == 2.0:
                #classList.append(x[0])
            if x[9] >= 0.17:
                classList.append(x[0])

        # 重複の削除およびソート
        necessaryList.sort()
        classList.sort()
        necessaryList = self.get_unique_list(necessaryList)
        classList = self.get_unique_list(classList)

        how_to_count_dic = pd.read_csv(
            "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\how_to_count_dic.csv")
        unit_dic = ['位', '宇', '折', '果', '箇', '荷', '菓', '掛', '顆', '回', '階', '画', '頭', '方', '株', '巻', '管', '缶', '基', '機', '騎', '切', '客', '脚', '行', '局', '句', '軀', '口', '具', '組', '景', '桁', '件', '軒', '個', '戸', '号', '合', '梱', '献', '喉', '座', '棹', '冊', '皿', '氏', '締', '字', '軸', '室', '首', '重', '床', '条', '畳', '錠', '帖', '筋', '食', '隻', '膳', '双',
                    '艘', '足', '揃', '体', '袋', '台', '題', '立', '卓', '束', '玉', '着', '丁', '挺', '帳', '張', 'つ', '対', '通', '番', '粒', '艇', '滴', '点', '度', '等', '堂', '人', '把', '羽', '張', '刎', '杯', '柱', '鉢', '発', '尾', '匹', '瓶', '振', '部', '幅', '服', '房', '篇', '遍', '本', '間', '枚', '前', '幕', '棟', '名', '面', '門', '問', '山', '葉', '流', '旒', '両', '領', '輪', '連', '椀', '碗','文']
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
    
        # 動詞の抽出
        operateList, necessaryList = self.methodGenerate.doins(classList, necessaryList,self.specName)

        # クラスとインスタンス変数の概念レベルを比較
        classInstanceList, otherList = self.instanceGenerate.doins(
            necessaryList, classList)
        
        self.vdmGenerate.doins(classInstanceList, operateList, otherList)

        outPath = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_" + self.specName
        # フォルダにアクセス権限を与え一旦削除
        if os.path.exists(outPath) == True:
            os.chmod(outPath, 755)
            shutil.rmtree(outPath)

        os.makedirs(outPath, exist_ok=True)
        # クラスとインスタンス変数の書き込み
        for i in range(len(classInstanceList)):
            classWord = classList[i]
            with open(outPath + "\\" + classWord + ".csv", 'w', encoding='utf8') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow([classWord])
                for j in range(len(classInstanceList[i][1])):
                    writer.writerow([classInstanceList[i][1][j]])

        # その他を書き込み
        with open(outPath + "\\necessary_word.csv", 'w', encoding='utf8') as f:
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


"""
    # リスト内の品詞を取得する
     m = MeCab.Tagger("-Ochasen")
        for x in new_list:
            nouns = m.parse(x[1]).splitlines()
            for i in range(len(nouns)):
                print(nouns[i].split())
            print('-----------------------------------')
"""
