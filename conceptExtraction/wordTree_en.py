from graphviz import Digraph
import pandas as pd
import csv
from collections import defaultdict

class treeGraph_en:

    def __init__(self, dict, semiList, word):
        self.dict = dict
        self.word = word
        self.semiList = semiList

    def display(self):
        print(self.dict)
        G = Digraph(format='png')
        G.attr('node', shape='circle')
        for key in self.dict.keys():
            G.node(key)
            for value in self.dict[key]:
                if value == 'null':
                    pass
                else:
                    G.edge(key, value)
        G.render(self.word)
        
                    



            
            
            
        
