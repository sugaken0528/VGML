import MeCab
m = MeCab.Tagger("-Ochasen")
nouns = m.parse("学生番号").splitlines()
for i in range(len(nouns)-1):
    print(nouns[i].split()[0])
