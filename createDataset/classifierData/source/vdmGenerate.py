import os
import shutil
import csv

class vdmGenerate:
    def __init__(self, specName):
        self.specName = specName

    def doins(self,classInstanceList,operateList,otherList):

        outPath = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\vdmData\\classifier_" + self.specName
        print(classInstanceList)
        # フォルダにアクセス権限を与え一旦削除
        if os.path.exists(outPath) == True:
            os.chmod(outPath, 755)
            shutil.rmtree(outPath)

        os.makedirs(outPath, exist_ok=True)
        self.otherVdm(otherList,outPath)
        self.classVdm(classInstanceList,operateList,outPath)

    def otherVdm(self,otherList,outPath):
        rows = []
        rows.append([])
        rows.append(['types'])
        rows.append([])
        rows.append(['values'])
        rows.append([])

        for x in otherList:
            if len(x) == 1:
                index = self.searchId(rows,"types")
                rows.insert(index,["  public " + str(x[0]) + " = real;"])
            elif len(x) == 2:
                index = self.searchId(rows,"values")
                rows.insert(index,["  " + str(x[0]) + " = " + str(x[1])])
        
        # その他を書き込み
        with open(outPath + "\\" + self.specName + ".vdmpp", 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["class " + self.specName])
            for x in rows:
                writer.writerow(x)
            writer.writerow(["end " + self.specName])
    
    def classVdm(self,classInstanceList,operateList,outPath):
        for classId in range(len(classInstanceList)):
            classWord = classInstanceList[classId][0][0]
            rows = []
            rows.append(['class ' + classWord])
            rows.append([])
            if self.instanceExis(classWord, classInstanceList):
                rows.append(['types'])
                rows.append([])
                rows.append(['instance variables'])
                rows.append([])
            if self.methodExis(classWord, operateList):
                rows.append(['operations'])
            rows.append(['end ' + classWord])
            for instanceId in range(len(classInstanceList[classId][1])):
                instanceWord = classInstanceList[classId][1][instanceId]
                typeWord = instanceWord.replace(classWord,'')
                index = self.searchId(rows, "instance variables")
                rows.insert(index,["  public " + instanceWord + " : " + typeWord + ";"])
                index = self.searchId(rows, "types")
                rows.insert(index,["  public " + typeWord + " = real;"])
            for operateId in range(len(operateList)):
                if classWord == operateList[operateId][0]:
                    operateWord = operateList[operateId][1]
                    index = self.searchId(rows, "operations")
                    rows.insert(index,["  public " + operateWord + " : () ==> real"])
                    rows.insert(index+1,["  " + operateWord + "()=="])
                    rows.insert(index+2,["  return 0;"])
                    rows.insert(index+3,[])

            # その他を書き込み
            with open(outPath + "\\" + classWord + ".vdmpp", 'w', encoding='utf8') as f:
                writer = csv.writer(f, lineterminator='\n')
                for x in rows:
                    writer.writerow(x)



    def searchId(self,rows,idWord):
        for i in range(len(rows)):
            if rows[i] != [] and idWord in rows[i][0]:
                return i+1

    def instanceExis(self, classWord, classInstanceList):
        count = 0
        for classId in range(len(classInstanceList)):
            if classWord == classInstanceList[classId][0][0] and len(classInstanceList[classId][1]) != 0:
                count += 1
        if count > 0:
            return True
        else:
            return False
    
    def methodExis(self, classWord, methodList):
        count = 0
        for i in range(len(methodList)):
            if methodList[i][0] == classWord:
                count += 1
        if count > 0:
            return True
        





