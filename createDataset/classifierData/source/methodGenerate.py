import MeCab


class methodGenerate:
    def __init__(self):
        pass

    def doins(self, necessaryList):
        m = MeCab.Tagger("-Ochasen")
        verbList = []  # 動詞化できる名詞を格納
        otherList = []  # 動詞化できる名詞以外を格納

        sahen = "名詞-サ変接続"
        for wordId in range(len(necessaryList)):
            nouns = m.parse(necessaryList[wordId][0]).splitlines()
            partOfSpeech = nouns[-2].split()[-1]
            if partOfSpeech == sahen:
                verbList.append(necessaryList[wordId])
            else:
                otherList.append(necessaryList[wordId])
        print(verbList)
        return verbList, necessaryList
