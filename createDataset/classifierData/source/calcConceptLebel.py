import sys
sys.setrecursionlimit(10000)
class CalcConceptLevel:
    def __init__(self, dict, semiList):
        self.dict = dict
        self.semiList = semiList
        self.sum = len(self.semiList)

    def doCalc(self):
        print(self.dict)
        print("-------------------------------------------------------------------------------")
        print(self.semiList)
        loopCount = 0
        for key in self.semiList:
            hierarchy = 0
            self.calc(key, loopCount, hierarchy)
        return self.sum

    def calc(self, key, loopCount,hierarchy):
        print("現在のsumは{}です".format(self.sum))
        semiList = self.dict[key]
        if 'null' not in semiList: #下位概念が存在する
            hierarchy += 1
            print("{}/{}".format(len(semiList),2**hierarchy))
            self.sum += len(semiList) / (2**hierarchy)
            for key in semiList:
                self.calc(key, loopCount, hierarchy)
        elif hierarchy >= 1: #下位概念が存在しない
            hierarchy -= 1
            return
        else:
            return



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