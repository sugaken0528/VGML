import pandas as pd
import numpy as np
import sys
sys.path.append('../extractedData/source')
from Morphological import Morphological

loadTxtName = sys.argv[1]
df = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\loadTxt\\"+loadTxtName+"_load.txt")
# 抽出データを文ごとにarrayに格納
docs = np.array([])
docs = np.append(docs, df.columns)
for x in df.values:
    docs = np.append(docs, x)
morphological = Morphological(docs, loadTxtName)
morphological.createParameta("teach")
