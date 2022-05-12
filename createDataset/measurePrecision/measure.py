import pandas as pd

anser = pd.read_csv("anser_intern.csv")
classifier = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_intern.csv")

anserList = []
duplicateList = []
classifierList = []

anserList.append(anser.columns[0])
duplicateList.append(classifier.columns[0])
for x in anser.values:
    anserList.append(x[0])

# 分類結果の単語名と
for x in classifier.values:
    tempList = [x[0], x[10]]
    duplicateList.append(tempList)
duplicateList.pop(0)

for i in range(len(duplicateList)-1):
    word = duplicateList[i][0]
    if(word == duplicateList[i+1][0]):
        pass
    else:
        classifierList.append(duplicateList[i])
classifierList.append(duplicateList[-1])

wordList = []
for x in classifierList:
    if(x[1] >= 1):
        wordList.append(x[0])
print(wordList)

count = 0
for x in wordList:
    if x in anserList:
        print(x)
        count += 1
print(count)
precision = count / len(anserList)
recall = count / len(classifierList)
print(precision)
print(recall)
f = (2*precision*recall) / (precision+recall)

print("適合率:{}".format(precision))
print("再現率:{}".format(recall))
print("F値:{}".format(f))
