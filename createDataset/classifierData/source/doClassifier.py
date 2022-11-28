from classifier import classifier
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\loadTxt\\advance_kyogi_load.txt")

# 変数名を変更中
# docs1 → specification
# docs → docsNumber

specification = np.array([])
for x in df.values:
    specification = np.append(specification, x)

docsNumber = np.array([])  # 数値を含む文章のみを格納するリスト
for x in df.values:
    if (any(map(str.isdigit, x[0]))):  # 文章が数値を含む場合
        docsNumber = np.append(docsNumber, x)

# 文章中の単語にTFI-DF値を付与
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(specification)
TF_list = vecs.toarray()  # (97,363) 97文章,363単語

words = vectorizer.get_feature_names_out()  # (363,) 単語のみを格納

doc_list = []
for sentence_id, vec in zip(range(len(specification)), TF_list):  # vec(363,)
    docs = []
    count = 0
    # TFI-DF値を昇順にソート
    for word_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True):
        lemma = words[word_id]
        if tfidf > 0.00:
            doc = [lemma, tfidf]
            docs.append(doc)
            count = count+1
    doc = [sentence_id, count]
    docs.insert(0, doc)
    doc_list.append(docs)

result = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\resultData\\result_classifier_advance.csv")

classifier = classifier(result, specification, docs, words, TF_list)
createClassifierList = classifier.createClassifierList()
