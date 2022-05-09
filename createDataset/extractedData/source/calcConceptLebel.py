class CalcConceptLevel:
    def __init__(self, dict, semiList):
        self.dict = dict
        self.semiList = semiList
        self.sum = 0

    def calc(self):
        count = 0
        for key in self.semiList:
            if 'null' not in self.dict[key]:
                for value in self.dict[key]:
                    self.sum += 1
                    print("{}の値{}".format(value, 1))
                    self.calc2(value, count)
        print(self.sum)

    def calc2(self, key, count):
        count += 1
        if key != 'null':
            for value in self.dict[key]:
                if value != 'null':
                    self.sum += 1/(2**count)
                    print("{}の値{}".format(value, 1/(2**count)))
                    self.calc2(value, count)
