# 指定した単語から上位概念を抽出する
import sqlite3
conn = sqlite3.connect("wnjpn.db")


class node:
    def __init__(self, name, children=None):
        self.name = name
        self.children = children

    # 結果表示用
    def display(self, indent=0):
        if self.children != None:
            print('-'*indent + self.name)
            for c in self.children:
                c.display(indent+1)
            else:
                print('-'*indent + self.name)


cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")

hierarchy_dict = {}

for row in cur:
    b_term = row[0]
    n_term = row[1]

    if n_term not in hierarchy_dict:
        hierarchy_dict[n_term] = b_term


def SearchTopConceptWords(word, hierarchy_dict):

    # 問い合わせた単語がwordNetに存在するかの確認
    cur = conn.execute("select wordid from word where lemma='%s'" % word)
    word_id = 99999999
    for row in cur:
        word_id = row[0]
        # print(word_id)

    # Wordnetに存在する単語であるかの判定
    if word_id == 99999999:
        print("[%s]は、WordNetに存在しない単語です。" % word)
        return
    else:
        print("[%s]の最上位概念を出力します\n" % word)

    # 入力された単語を含む概念を検索する
    cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して出力する
    no = 1
    for synset in synsets:
        cur1 = conn.execute(
            "select name from synset where synset='%s'" % synset)
        for row1 in cur1:
            print("%sつ目の概念 : %s" % (no, row1[0]))
            cur2 = conn.execute(
                "select def from synset_def where (synset='%s' and lang='jpn')" % synset)
            sub_no = 1
            for row2 in cur2:
                print("意味%s : %s" % (sub_no, row2[0]))
                sub_no += 1

        # 上位語の検索
        while(synset in hierarchy_dict.keys()):
            lowerSynset = synset
            synset = hierarchy_dict[synset]
            cur1 = conn.execute(
                "select name from synset where synset='%s'" % synset)
            cur11 = conn.execute(
                "select name from synset where synset='%s'" % lowerSynset)
            for row1 in cur1:
                for row11 in cur11:
                    print("'%s'の上位概念 : %s" % (row11[0], row1[0]))

            cur2 = conn.execute(
                "select def from synset_def where (synset='%s' and lang='jpn')" % synset)
            sub_no = 1
            for row2 in cur2:
                print("意味%s : %s" % (sub_no, row2[0]))
                sub_no += 1

        # 更新
        print("\n")
        no += 1


SearchTopConceptWords("大企業", hierarchy_dict)
