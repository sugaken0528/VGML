class CalcConceptLevel:
    def __init__(self, dict, semiList):
        self.dict = dict
        self.semiList = semiList
        self.sum = 0
        self.loopCount = 0

    def calc(self):
        self.loopCount = 0
        count = 0
        for key in self.semiList:
            if 'null' not in self.dict[key]:
                for value in self.dict[key]:
                    self.sum += 1
                    #print("{}の値{}".format(value, 1))
                    if self.loopCount <= 5000:
                        self.calc2(value, count)
        print(self.sum)
        return self.sum

    def calc2(self, key, count):
        print(self.loopCount)
        if key != 'null' and count:
            for value in self.dict[key]:
                if value != 'null' and count:
                    self.sum += 1/(2**count)
                    #print("{}の値{}".format(value, 1/(2**count)))
                    if self.loopCount <= 5000:
                        self.calc2(value, count)
