import sqlite3
from collections import defaultdict
conn = sqlite3.connect("wnjpn.db")
word='月'
cur = conn.execute(
    "select synset1,synset2 from synlink where link='hypo'")
hierarchy_dict = defaultdict(list)
for row in cur:
    hyperTerm = row[0]
    lowerTerm = row[1]
    hierarchy_dict[hyperTerm].append(lowerTerm)            

# 問い合わせた単語がwordNetに存在するかの確認
cur = conn.execute(
    "select wordid from word where lemma='%s'" % word)
word_id = 99999999
for row in cur:
    word_id = row[0]

# Wordnetに存在する単語であるかの判定
if word_id == 99999999:
    print("[%s]は、WordNetに存在しない単語です。" % word)
else:
    print("[%s]の下位概念を出力します\n" % word)
# 入力された単語を含む概念を検索する
cur = conn.execute(
            "select synset from sense where wordid='%s' AND lang='jpn'" % word_id)
synsets = []
for row in cur:
    synsets.append(row[0])
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