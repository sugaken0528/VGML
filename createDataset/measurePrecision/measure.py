import pandas as pd

anser = pd.read_csv("anser_intern.csv")
classAnser = pd.read_csv("anser_class.csv")
classifier = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_intern.csv")

anserList = []  # 正解の単語
anserClassList = []  # 正解のクラスの単語
duplicateList = []  # 重複を含む分類リスト
classifierList = []  # 重複を削除した分類リスト

anserList.append(anser.columns[0])
anserClassList.append(classAnser.columns[0])
duplicateList.append(classifier.columns[0])
for x in anser.values:
    anserList.append(x[0])
for x in classAnser.values:
    anserClassList.append(x[0])
print(anserClassList)
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
classList = []
for x in classifierList:
    if(x[1] >= 1):
        wordList.append(x[0])
    if(x[1] == 2):
        classList.append(x[0])
print(wordList)

count = 0
for x in wordList:
    if x in anserList:
        print(x)
        count += 1
print("一致した単語数は{}個です".format(count))
precision = count / len(anserList)
recall = count / len(classifierList)
f = (2*precision*recall) / (precision+recall)
print("単語の適合率:{}".format(precision))
print("単語の再現率:{}".format(recall))
print("単語のF値:{}".format(f))
print("\n")

count = 0
for x in classList:
    if x in anserClassList:
        print(x)
        count += 1
print("一致したクラス数は{}個です".format(count))
precision = count / len(anserClassList)
recall = count / len(classList)
f = (2*precision*recall) / (precision+recall)
print("単語の適合率:{}".format(precision))
print("単語の再現率:{}".format(recall))
print("単語のF値:{}".format(f))
