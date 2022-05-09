import re
import MeCab
import pandas as pd

result = pd.read_csv("extractedData/extracted_list_internValue_short.csv")
newList = []
newList.append(result.columns[1:])
tempList = []
for i in result.values:
    tempList = i[1:]
    newList.append(tempList)
