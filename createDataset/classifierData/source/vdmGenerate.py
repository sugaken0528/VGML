import os
import shutil
import csv

class vdmGenerate:
    def __init__(self, specName):
        self.specName = specName

    def doins(self,classInstanceList,classVerbList,otherList):
        rows = []
        rows.append([])
        rows.append(['types'])
        rows.append([])
        rows.append(['values'])
        rows.append([])

        for x in otherList:
            if len(x) == 1:
                index = self.searchId(rows,"types")
                print(index)
                rows.insert(index,["  public " + str(x[0]) + " = real;"])
            elif len(x) == 2:
                index = self.searchId(rows,"values")
                rows.insert(index,["  " + str(x[0]) + " = " + str(x[1])])
        print(rows)
        outPath = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\vdmData\\classifier_" + self.specName

        # フォルダにアクセス権限を与え一旦削除
        if os.path.exists(outPath) == True:
            os.chmod(outPath, 755)
            shutil.rmtree(outPath)

        os.makedirs(outPath, exist_ok=True)
        # その他を書き込み
        with open(outPath + "\\" + self.specName + ".vdmpp", 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["class " + self.specName])
            for x in rows:
                writer.writerow(x)
            writer.writerow(["end " + self.specName])

    def searchId(self,rows,idWord):
        for i in range(len(rows)):
            if rows[i] != [] and idWord in rows[i][0]:
                return i+1


