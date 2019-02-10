# -*- coding: utf-8 -*-
from graphviz import Digraph

class drawGraph:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def draw(self, data):
        pass

    def testDraw(self):
        dot = Digraph(comment="Thre round Table")
        dot.node('A', 'King')
        dot.node('B', 'Knight')
        dot.node('C', 'Solider')
        dot.edges(['AB','AC'])

        print(dot.source)
        dot.render(filename="./result.gv", format="png")