from classifier import classifier
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("loadTxt/advance_kyogi_load.txt")
docs1 = np.array([])
for x in df.values:
    docs1 = np.append(docs1, x)
docs = np.array([])
for x in df.values:
    if (any(map(str.isdigit, x[0]))):
        docs = np.append(docs, x)

vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(docs1)
TF_list = vecs.toarray()

words = vectorizer.get_feature_names_out()

doc_list = []
for doc_id, vec in zip(range(len(docs)), vecs.toarray()):
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
vectorizer.fit(docs1)

# 抽出した単語を確認する
wlist1 = vectorizer.get_feature_names_out()
# ['a', 'am', 'and', 'are', 'i', 'man', 'perfect', 'regend', robot', 'sam', 'you']
# 単語のリスト化
countlist = [0] * len(wlist1)

result = pd.read_csv("resultData/result_advance_kyogi.csv")

classifier = classifier(result, docs1, docs, wlist1, TF_list)
createClassifierList = classifier.createClassifierList()
