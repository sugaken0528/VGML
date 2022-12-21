# -*- coding: utf-8 -*-
from lowerWord import LowerWord
#from wordTree_en import treeGraph_en
from calcConceptLebel import CalcConceptLevel

word = '学生'
lowerWord = LowerWord()
dict, semiList = lowerWord.SearchTopConceptWords(word)  # 上位概念の辞書と同義語のリストを取得
# print(dict)
#treeGraph = treeGraph_en(dict, semiList, word)
#display = treeGraph.display()
calcConceptLebel = CalcConceptLevel(dict, semiList)
calc = calcConceptLebel.doCalc()
print(calc)
