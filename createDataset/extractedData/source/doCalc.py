# -*- coding: utf-8 -*-
from lowerWord import lowerWord
#from wordTree_en import treeGraph_en
from calcConceptLebel import CalcConceptLevel

word = '学生'
lowerWord = lowerWord()
dict, semiList = lowerWord.SearchTopConceptWords(word)
# print(dict)
#treeGraph = treeGraph_en(dict, semiList, word)
#display = treeGraph.display()
calcConceptLebel = CalcConceptLevel(dict, semiList)
calc = calcConceptLebel.calc()
