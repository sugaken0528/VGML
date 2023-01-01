import sys

class CalcConceptLevel:
    def __init__(self, dict, semiList):
        self.dict = dict
        self.semiList = semiList
        self.sum = 0
        self.loopCount = 0

    def doCalc(self):
        #print(self.dict)
        #print("-------------------------------------------------------------------------------")
        #print(self.semiList)
        for key in self.semiList:
            hierarchy = 0
            lowerList = self.dict[key]
            if 'null' not in lowerList:
                self.calc(key, hierarchy,lowerList)
        return self.sum

    def calc(self, key, hierarchy, lowerList):
        self.loopCount += 1
        if self.loopCount < 5000:
            #print("現在のsumは{}です".format(self.sum))
            #print("{}/{}".format(len(lowerList),2**hierarchy))
            self.sum += len(lowerList) / (2**hierarchy)
            for key in lowerList:
                lowerList2 = self.dict[key]
                if 'null' not in lowerList2 and self.loopCount < 5000: #下位概念が存在する
                    hierarchy += 1
                    self.calc(key, hierarchy,lowerList2)
                elif 'null' in lowerList2: #下位概念が存在しない
                    pass
                elif 'null' in lowerList2 and key == lowerList[-1]: #下位概念が存在しないかつlowerListの末尾の要素である
                    hierarchy -= 1
        else:
            return self.sum



"""
        for key in self.semiList:
            if 'null' not in self.dict[key]:
                for value in self.dict[key]:
                    sum += 1
                    #print("{}の値{}".format(value, 1))
                    if loopCount <= 5000:
                        self.calc2(sum, loopCount, value, count)
        # print(self.sum)
        return sum

    def calc(self, sum, loopCount, key, count):
        if key != 'null' and count:
            for value in self.dict[key]:
                if value != 'null' and count:
                    sum += 1/(2**count)
                    #print("{}の値{}".format(value, 1/(2**count)))
                    if loopCount <= 5000:
                        self.calc2(sum, loopCount, value, count)
"""