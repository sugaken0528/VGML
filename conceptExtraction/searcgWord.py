import sqlite3
conn = sqlite3.connect("wnjpn.db")
"""
cur = conn.execute("select name from synset where synset='01108753-n'")
for row in cur:
    word_id = row[0]
    print(row[0])
cur = conn.execute("select name from synset where synset='00213343-n'")
for row in cur:
    word_id = row[0]
    print(row[0])
cur = conn.execute("select name from synset where synset='01108971-n'")
for row in cur:
    word_id = row[0]
    print(row[0])
"""
cur = conn.execute("select name from synset where synset='01108753-n'")
print(cur[0])
