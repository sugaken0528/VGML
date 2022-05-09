
import pandas as pd
import csv
import numpy as np
result = pd.read_csv("teach_intern_short.csv")
newList = []
newList.append(result.columns[1:])
tempList = []
for i in result.values:
    tempList = i[1:]
    newList.append(tempList)

with open("teach_internValue_short.csv", 'w', encoding='utf8') as f:
    writer = csv.writer(f, lineterminator='\n')
    for x in newList:
        writer.writerow(x)
