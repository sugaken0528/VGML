import MeCab
m = MeCab.Tagger("-Ochasen")
nouns = m.parse("同メールアドレス").splitlines()
for i in range(len(nouns)-1):
    print(nouns[i].split()[0])
    print(nouns[i].split()[1])
    print(nouns[i].split()[2])
    print(nouns[i].split()[3])
    print(nouns[i].split()[-1])
    print("--------------------------------------")
