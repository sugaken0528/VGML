import sqlite3
conn = sqlite3.connect("wnjpn.db")

cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")

for row in cur:
    hyper_term = row[0]
    hypo_term = row[1]
