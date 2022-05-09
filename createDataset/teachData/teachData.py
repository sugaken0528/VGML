# -*- coding: utf-8 -*-
import csv
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import MeCab
import numpy as np


class teachData:
    def __init__(self, docs):
        self.docs = docs

    def createParameta(self):
        #docs = self.wordOrganization()
        docs = self.docs
        parametaList = self.tfidf(docs)
        parametaList = self.priority(parametaList)
        parametaList = self.Linking(parametaList)
        #parametaList = self.koyu(parametaList)
        #parametaList = self.delete(parametaList)
        parametaList = self.duplicateDeletion(parametaList)
        # 判定結果を追加
        for x in parametaList:
            x.insert(1, "0")
        new_list = sorted(parametaList, reverse=True)
        list_ = ["単語", "判定結果", "TF-IDF値", "出現回数", "優先値", "連結回数", "固有度"]
        new_list.insert(0, list_)

        with open("teach_advance_kyogi.csv", 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            for x in new_list:
                writer.writerow(x)

    def wordOrganization(self):
        exclusionList = ['/', '\\', '(', ')', '[', ']', '{', '}']
        hiziritushi = '名詞-非自立'
        setuzokushi = '接続詞'
        rentaishi = '連体詞'
        settoshi = '接頭詞'
        sahen = '名詞-サ変接続'
        setubishi = '接尾詞'
        hukushikano = '名詞-副詞可能'
        m = MeCab.Tagger("-Ochasen")
        word = ''
        resultWords = []
        for i in range(len(self.docs)):
            tempList = []
            for char in self.docs[i]:
                if(char != ' ' and '記号' not in m.parse(char).splitlines()[-2].split()[-1] and char not in exclusionList):
                    word += char
                elif(char == ' ' and word != ' '):
                    nouns = m.parse(word).splitlines()
                    nouns.pop(-1)
                    hiragana = re.findall("[ぁ-ん]", nouns[-1].split()[0])
                    if(hukushikano in nouns[-1].split()[-1] or rentaishi in nouns[-1].split()[-1] or setubishi in nouns[-1].split()[-1] or len(hiragana) == len(nouns[-1].split()[0])):
                        nouns.pop(-1)
                    elif(rentaishi in nouns[0].split()[-1] or setuzokushi in nouns[0].split()[-1] or hiziritushi in nouns[0].split()[-1] or settoshi in nouns[0].split()[-1] or hukushikano in nouns[0].split()[-1]):
                        nouns.pop(0)
                    tempWord = ''
                    """
                    flag = 0
                    for c in range(len(nouns)-1):
                        if('名詞-一般' in nouns[c].split()[-1] and sahen in nouns[c+1].split()[-1]):
                            flag = 1
                            flagNum = c
                    if(flag == 1):
                        del nouns[flagNum+1:]
                    """
                    for j in range(len(nouns)):
                        tempWord += nouns[j].split()[0]
                    if(tempWord != ''):
                        tempList.append(tempWord)
                    word = ' '
            resultWords.append(tempList)

        newList = np.array([])
        words = ''
        for sentence in resultWords:
            for word in sentence:
                words += word + ' '
            newList = np.append(newList, words)
            words = ''
        # print(newList)
        return newList
        # 各単語にTFI-DF値を付与

    def tfidf(self, inidocs):
        vectorizer = TfidfVectorizer(
            use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
        vecs = vectorizer.fit_transform(inidocs)
        TF_list = vecs.toarray()
        words = vectorizer.get_feature_names_out()
        # words = self.wordOrganization(words)
        doc_list = []
        for doc_id, vec in zip(range(len(inidocs)), vecs.toarray()):
            docs = []
            count = 0
            for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True):
                lemma = words[w_id]
                if tfidf > 0.00:
                    doc = [lemma, tfidf]
                    docs.append(doc)
                    count = count+1
            doc = [doc_id, count]
            docs.insert(0, doc)
            doc_list.append(docs)
        # vectorizeする
        vectorizer.fit(inidocs)
        # 抽出した単語を確認する
        wlist1 = vectorizer.get_feature_names_out()
        # 単語のリスト化
        countlist = [0] * len(wlist1)
        # 単語とTF-IDF値の追加
        i = 0
        lists = []
        for x in TF_list:
            for y in x:
                if y > 0.0:
                    tempList = []
                    tempList.append(wlist1[i])
                    tempList.append(y)
                    countlist[i] = countlist[i]+1
                    lists.append(tempList)
                i = i+1
            i = 0
        lists.sort()

        # 出現回数の付与
        tempList = []
        for x in lists:
            for j, y in enumerate(wlist1):
                if x[0] == y:
                    x.append(countlist[j])

        lists = [x for x in lists if (len(x[0]) != 1) or len(
            re.findall("[一-龥]", x[0])) == 1]
        lists = [x for x in lists if len(x[0]) < 20]
        return lists

    # 優先値の付与
    def priority(self, lists):
        # 優先値の追加
        for x in lists:
            weight = 0
            # ひらがなの抽出
            hiragana = re.findall("[ぁ-ん]", x[0])
            # カタカナの抽出
            katakana = re.findall("[ァ-ン]", x[0])
            # 漢字の抽出
            kanji = re.findall("[一-龥]", x[0])

            haifun = re.findall("[ー]", x[0])

            eigo = re.findall("[a-z]", x[0])

            suuzi = re.findall("[a-z]", x[0])

            weight = len(hiragana)*0.1+(len(haifun)+len(eigo) +
                                        len(suuzi))*0.2+len(katakana)*0.5 + len(kanji)*0.5

            x.append(weight)
        return lists

    # 連結回数を付与
    def Linking(self, lists):
        for x in lists:
            count = 0
            for y in lists:
                for z in y:
                    if type(z) is str:
                        if x[0] in z and x[0] != z:
                            count = count+1
            x.append(count)
        return lists

    def koyu(self, lists):
        koyumeshi = '名詞-固有名詞-組織'
        m = MeCab.Tagger("-Ochasen")
        for x in lists:
            count = 0
            nouns = m.parse(x[0]).splitlines()
            nouns.pop(-1)
            for i in range(len(nouns)):
                if(koyumeshi in nouns[i].split()[-1]):
                    count += 1
            if(count != 0):
                koyuLevel = count / len(nouns)
            else:
                koyuLevel = 0
            x.append(koyuLevel)
        return lists

    def delete(self, lists):
        m = MeCab.Tagger("-Ochasen")
        """
        for x in lists:
            nouns = m.parse(x[0]).splitlines()
            for i in range(len(nouns)):
                print(nouns[i].split())
            print('-----------------------------------')
        """
        daimeshi = '代名詞'
        meishi = '名詞'
        hukushikano = '副詞可能'
        hukushi = '副詞-一般'
        suzi = '名詞-数'
        kandoshi = '感動詞'
        sahen = '名詞-サ変'
        keiyodoshi = '名詞-形容動詞語幹'

        newList = []
        for x in lists:
            nouns = m.parse(x[0]).splitlines()
            nouns.pop(-1)
            if((len(nouns) == 1 and sahen in nouns[0].split()[-1]) or kandoshi in nouns[0].split()[-1] or daimeshi in nouns[0].split()[-1] or daimeshi in nouns[-1].split()[-1] or hukushi in nouns[0].split()[-1] or hukushi in nouns[-1].split()[-1] or len(nouns[0].split()) == 6 or (meishi in nouns[-1].split()[-1] and hukushikano in nouns[-1].split()[-1]) or keiyodoshi in nouns[-1].split()[-1]):
                continue
            if(len(nouns) != 1 and suzi in nouns[0].split()[-1]):
                continue
            if(len(nouns) >= 2 and ((nouns[0].split()[0] == '図' or nouns[0].split()[0] == '表') and suzi in nouns[1].split()[-1])):
                continue
            newList.append(x)
        """
        for x in newList:
            nouns = m.parse(x[0]).splitlines()
            for i in range(len(nouns)):
                print(nouns[i].split())
            print('-----------------------------------')
        """
        return newList

    def duplicateDeletion(self, lists):
        word = lists[0][0]
        value = 0
        newList = []
        count = 0
        for i in range(len(lists)):
            print(lists[i][0])
            if(word == lists[i][0]):
                value += lists[i][1]
                count += 1
                if(i+1 > len(lists)-1):
                    lists[i][1] = value / count
                    newList.append(lists[i])
            else:
                lists[i-1][1] = value / (count)
                newList.append(lists[i-1])
                word = lists[i][0]
                value = lists[i][1]
                count = 1
        return newList
