from classifier import classifier
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\loadTxt\\advance_kyogi_load.txt")

specification = np.array([])
for x in df.values:
    specification = np.append(specification, x)

# 文章中の単語にTFI-DF値を付与
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(specification)
TF_list = vecs.toarray()  # (97,363) 97文章,363単語

wordList = vectorizer.get_feature_names_out()  # (363,) 単語のみを格納

result = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\resultData\\result_classifier_advance.csv")

classifier = classifier(result, specification, wordList, TF_list)
createClassifierList = classifier.createClassifierList()
