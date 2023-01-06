import MeCab
m = MeCab.Tagger("-Ochasen")
nouns = m.parse("項目は、年度、企業名、企業担当者ID、企業担当者名、企業担当者連絡先電話番号、同メールアドレスの4つとすること。").splitlines()
for i in range(len(nouns)-1):
    print(nouns[i].split()[0])
    print("--------------------------------------")
