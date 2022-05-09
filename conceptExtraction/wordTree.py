from graphviz import Digraph
from googletrans import Translator
import pandas as pd
import csv
from collections import defaultdict

class treeGraph:

    def __init__(self, dict, semiList, word):
        self.dict = dict
        self.word = word
        self.semiList = semiList
        self.translator = Translator()
        self.transDict = {}

    def display(self):
        newDict = self.translation()
        #print(self.dict)
        print(newDict)
        G = Digraph(format='png')
        G.attr('node', shape='circle')
        for key in newDict.keys():
            G.node(key)
            for value in newDict[key]:
                if value == 'null':
                    pass
                else:
                    G.edge(key, value)
        G.render(self.word)
    
    def translation(self):
        for key in self.dict.keys():
            repKey = key.replace('_', ' ')
            key = self.translator.translate(repKey, dest='ja', src='en').text
            self.transDict[repKey] = key
        print(self.transDict)
        newDict = defaultdict(list)
        for key in self.dict.keys():
            tempList = []
            for value in self.dict[key]:
                #英語の場合'null'日本語の場合''
                if value == 'null':
                    pass
                else:
                    value = self.transDict[value.replace('_', ' ')]
                    tempList.append(value)
            key = self.transDict[key.replace('_', ' ')]
            if key in newDict.keys():
                for i in range(len(tempList)):
                    newDict[key].append(tempList[i])
            else:
                newDict[key] = tempList
        return newDict
                
        
                    



            
            
            
        
