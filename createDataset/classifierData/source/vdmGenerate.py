import os
import shutil
import csv

class vdmGenerate:
    def __init__(self, specName):
        self.specName = specName

    def doins(self,classInstanceList,operateList,otherList):

        outPath = "\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\vdmData\\classifier_" + self.specName
        # フォルダにアクセス権限を与え一旦削除
        if os.path.exists(outPath) == True:
            os.chmod(outPath, 755)
            shutil.rmtree(outPath)

        os.makedirs(outPath, exist_ok=True)
        self.otherVdm(otherList,outPath)
        self.classVdm(classInstanceList,operateList,outPath)

    def otherVdm(self,otherList,outPath):
        newOtherList = []
        for i in range(len(otherList)):
            wordSet = self.unitCheck(otherList[i])
            newOtherList.append(wordSet)

        rows = []
        rows.append([])
        rows.append(['types'])
        rows.append([])
        rows.append(['values'])
        rows.append([])
        print(newOtherList)
        for x in newOtherList:
            if len(x) == 1:
                index = self.searchId(rows,"types")
                rows.insert(index,["  public " + str(x[0]) + " = real;"])
            elif len(x) == 2:
                index = self.searchId(rows,"values")
                rows.insert(index,["  " + str(x[0]) + " = " + str(x[1])+";"])
        # その他を書き込み
        with open(outPath + "\\" + self.specName + ".vdmpp", 'w', encoding='utf8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["class " + self.specName])
            for x in rows:
                writer.writerow(x)
            writer.writerow(["end " + self.specName])
    
    def classVdm(self,classInstanceList,operateList,outPath):
        for classId in range(len(classInstanceList)):
            typeList = []
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
                if typeWord in typeList:
                    print("{}は{}に含まれます".format(typeWord,typeList))
                else:
                    index = self.searchId(rows, "types")
                    rows.insert(index,["  public " + typeWord + " = real;"])
                    typeList.append(typeWord)
            for operateId in range(len(operateList)):
                if classWord == operateList[operateId][0]:
                    operateWord = operateList[operateId][1]
                    index = self.searchId(rows, "operations")
                    rows.insert(index,["  public " + operateWord + " : () ==> real"])
                    rows.insert(index+1,["  " + operateWord + "()=="])
                    rows.insert(index+2,["  is not yet specified;"])
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
        
    def unitCheck(self, otherSet):
        unit_dic = ['位', '宇', '折', '果', '箇', '荷', '菓', '掛', '顆', '回', '階', '画', '頭', '方', '株', '巻', '管', '缶', '基', '機', '騎', '切', '客', '脚', '行', '局', '句', '軀', '口', '具', '組', '景', '桁', '件', '軒', '個', '戸', '号', '合', '梱', '献', '喉', '座', '棹', '冊', '皿', '氏', '締', '字', '軸', '室', '首', '重', '床', '条', '畳', '錠', '帖', '筋', '食', '隻', '膳', '双',
                    '艘', '足', '揃', '体', '袋', '台', '題', '立', '卓', '束', '玉', '着', '丁', '挺', '帳', '張', 'つ', '対', '通', '番', '粒', '艇', '滴', '点', '度', '等', '堂', '人', '把', '羽', '張', '刎', '杯', '柱', '鉢', '発', '尾', '匹', '瓶', '振', '部', '幅', '服', '房', '篇', '遍', '本', '間', '枚', '前', '幕', '棟', '名', '面', '門', '問', '山', '葉', '流', '旒', '両', '領', '輪', '連', '椀', '碗','文']
        for dic in range(len(unit_dic)):
                if unit_dic[dic] in otherSet[0] and any(map(str.isdigit, otherSet[0])):
                    for j in range(len(otherSet[0])):
                        if otherSet[0][j] == unit_dic[dic]:
                            word = otherSet[0][j+1:]
                            if len(otherSet) >= 2:
                                suti = otherSet[1]
                                wordSet = [word, suti]
                                return wordSet
                            else:
                                wordSet = [word]
                                return wordSet
        word = otherSet[0]
        if len(otherSet) >= 2:
            suti = otherSet[1]
            wordSet = [word, suti]
        else:
            wordSet = [word]
        return wordSet

        





