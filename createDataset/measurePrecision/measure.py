import pandas as pd

anser = pd.read_csv("anser_kyogi.csv")
classAnser = pd.read_csv("anser_kyogi_class.csv")
classifier = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance.csv")

anserList = []  # 正解の単語
anserClassList = []  # 正解のクラスの単語
classifierList = []  # 重複を削除した分類リスト

anserList.append(anser.columns[0])
anserClassList.append(classAnser.columns[0])
classifierList.append(classifier.columns[1])

for x in anser.values:
    anserList.append(x[0])

for x in classAnser.values:
    anserClassList.append(x[0])

# 分類結果の単語名と
for x in classifier.values:
    classifierList.append(x[1])

count = 0
for x in classifierList:
    if x in anserList:
        print(x)
        count += 1
print(count)

print("一致した単語数は{}個です".format(count))
precision = count / len(anserList)
recall = count / len(classifierList)
f = (2*precision*recall) / (precision+recall)
print("単語の適合率:{}".format(precision))
print("単語の再現率:{}".format(recall))
print("単語のF値:{}".format(f))
print("\n")


classData = pd.read_csv(
    "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_advance_class.csv")

classList = []
classList.append(classData.columns[0])
for x in classData.values:
    classList.append(x[0])
print(classList)
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
