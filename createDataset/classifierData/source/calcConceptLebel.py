class CalcConceptLevel:
    def __init__(self, dict, semiList):
        self.dict = dict
        self.semiList = semiList

    def calc(self):
        loopCount = 0
        sum = 0
        count = 0
        for key in self.semiList:
            if 'null' not in self.dict[key]:
                for value in self.dict[key]:
                    sum += 1
                    #print("{}の値{}".format(value, 1))
                    if loopCount <= 5000:
                        self.calc2(sum, loopCount, value, count)
        # print(self.sum)
        return sum

    def calc2(self, sum, loopCount, key, count):
        # print(self.loopCount)
        if key != 'null' and count:
            for value in self.dict[key]:
                if value != 'null' and count:
                    sum += 1/(2**count)
                    #print("{}の値{}".format(value, 1/(2**count)))
                    if loopCount <= 5000:
                        self.calc2(sum, loopCount, value, count)
