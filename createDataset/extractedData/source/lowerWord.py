# -*- coding: utf-8 -*-
# 指定した単語から下位概念を抽出する
import sqlite3
from collections import defaultdict


class lowerWord:

    def __init__(self):
        self.conn = sqlite3.connect("../../wnjpn.db")
        self.hierarchy_dict = defaultdict(list)  # 上位語を指定して下位語のリストを取得できる辞書
        self.tree_dict = defaultdict(list)
        self.semi_hyper_list = []

    def SearchTopConceptWords(self, word):
        # 下位語検索用の辞書を作成
        cur = self.conn.execute(
            "select synset1,synset2 from synlink where link='hypo'")
        self.hierarchy_dict = defaultdict(list)
        count = 0
        for row in cur:
            hyperTerm = row[0]
            lowerTerm = row[1]
            # print(row)
            count += 1
            self.hierarchy_dict[hyperTerm].append(lowerTerm)
        # print(count)

        # 問い合わせた単語がwordNetに存在するかの確認
        cur = self.conn.execute(
            "select wordid from word where lemma='%s'" % word)
        word_id = 99999999
        for row in cur:
            word_id = row[0]

        # Wordnetに存在する単語であるかの判定
        if word_id == 99999999:
            print("[%s]は、WordNetに存在しない単語です。" % word)
            return
        else:
            print("[%s]の下位概念を出力します\n" % word)

        # 入力された単語を含む概念を検索する
        cur = self.conn.execute(
            "select synset from sense where wordid='%s'" % word_id)
        synsets = []
        for row in cur:
            synsets.append(row[0])  # 概念のidを格納

        # 概念に含まれる単語を検索して出力する
        conceptList = []
        for synset in synsets:
            cur1 = self.conn.execute(
                "select name from synset where synset='%s'" % synset)
            for row1 in cur1:
                conceptList.append(row1[0])  # 概念のnameを格納
        no = 1
        for synset in synsets:
            cur1 = self.conn.execute(
                "select name from synset where synset='%s'" % synset)
            for row1 in cur1:
                #print("%sつ目の概念 : %s" % (no, row1[0]))
                self.semi_hyper_list.append(row1[0])
                cur2 = self.conn.execute(
                    "select def from synset_def where (synset='%s' and lang='jpn')" % synset)  # 概念の意味を検索
                sub_no = 1
                for row2 in cur2:
                    # print("意味%s : %s" % (sub_no, row2[0]))  # 概念の意味を出力
                    sub_no += 1

            # 下位語の検索
            highperSynset = synset  # 上位語(id)
            lowList = self.hierarchy_dict[synset]  # 下位語(name)
            synsetList = []
            for i in range(len(lowList)):
                cur = self.conn.execute(
                    "select name from synset where synset='%s'" % lowList[i])
                for row in cur:
                    # 下位語が上位語と同じだった場合
                    if row[0] in conceptList:
                        pass
                    else:
                        synsetList.append(lowList[i])

            self.extract(highperSynset, synsetList, conceptList)
            # 更新
            # print("\n")
            no += 1
        return self.tree_dict, self.semi_hyper_list

    def extract(self, highperSynset, synsetList, conceptList):
        cur1 = self.conn.execute(
            "select name from synset where synset='%s'" % highperSynset)  # 上位語の名前を検索
        if len(synsetList) == 0:  # 下位語がなかった場合
            for row1 in cur1:
                self.tree_dict[row1[0]].append('null')  # 上位語の下位語をnullとする
                #print("%sに下位概念は存在しません" % row1[0])
        else:
            cur1 = self.conn.execute(
                "select name from synset where synset='%s'" % highperSynset)
            for row in cur1:
                #print("'%s'の下位概念" % row[0])
                hyper = row[0]
            for i in range(len(synsetList)):
                cur2 = self.conn.execute(
                    "select name from synset where synset='%s'" % synsetList[i])
                for row2 in cur2:
                    self.tree_dict[hyper].append(row2[0])
                    #print("%s" % row2[0])
                """
                # 下位概念の説明
                cur3 = self.conn.execute(
                    "select def from synset_def where (synset='%s' and lang='jpn')" % synsetList[i])
                sub_no = 1
                for row3 in cur3:
                    #print("意味%s : %s" % (sub_no, row3[0]))
                    sub_no += 1
                """
            for i in range(len(synsetList)):  # 各下位語を探索する
                highperSynset = synsetList[i]  # 下位語を上位語とする
                lowerList = self.hierarchy_dict[highperSynset]  # 上位語の下位語リストを取得
                # 下位語の中に最上位の概念が含まれる可能性がある為、その場合は省く
                newLowerList = []
                for j in range(len(lowerList)):
                    cur = self.conn.execute(
                        "select name from synset where synset='%s'" % lowerList[j])
                    for row in cur:
                        if row[0] in conceptList:
                            pass
                        else:
                            newLowerList.append(lowerList[j])
                self.extract(highperSynset, newLowerList, conceptList)
