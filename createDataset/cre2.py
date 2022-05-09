
import pandas as pd
import csv
import numpy as np
origin = pd.read_csv("extractedData/extracted_list_intern_short.csv")
value = pd.read_csv("resultData/result_internValue_short.csv")
newList = []
newList.append(origin.columns.append(value.columns[6:]))
tempList = []
valueList = []
for i in range(len(origin.values)):
    newList.append(np.append(origin.values[i], value.values[i][6:]))

with open("resultData/result_intern_short.csv", 'w', encoding='utf8') as f:
    writer = csv.writer(f, lineterminator='\n')
    for x in newList:
        writer.writerow(x)
