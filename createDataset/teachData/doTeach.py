from teachData import teachData
import pandas as pd
import numpy as np
df = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\loadTxt\\intern_load.txt")
# 抽出データを文ごとにarrayに格納
docs = np.array([])
docs = np.append(docs, df.columns)
for x in df.values:
    docs = np.append(docs, x)
morphological = teachData(docs)
morphological.createParameta()
