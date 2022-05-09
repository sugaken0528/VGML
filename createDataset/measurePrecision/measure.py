import pandas as pd

anser = pd.read_csv("anser_kyogi.csv")
classifier = pd.read_csv("../classifierData/classifier_advance.csv")

anserList = []
classifierList = []

anserList.append(anser.columns[0])
classifierList.append(classifier.columns[1])

for x in anser.values:
    anserList.append(x[0])

for x in classifier.values:
    classifierList.append(x[1])

count = 0
for x in classifierList:
    if x in anserList:
        print(x)
        count += 1
print(count)
precision = count / len(anserList)
recall = count / len(classifierList)
f = (2*precision*recall) / (precision+recall)

print("適合率:{}".format(precision))
print("再現率:{}".format(recall))
print("F値:{}".format(f))
