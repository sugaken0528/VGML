from teachData import teachData
import pandas as pd
import numpy as np
df = pd.read_csv("../loadTxt/advance_kyogi_load.txt")
# 抽出データを文ごとにarrayに格納
docs = np.array([])
docs = np.append(docs, df.columns)
for x in df.values:
    docs = np.append(docs, x)
morphological = teachData(docs)
morphological.createParameta()
