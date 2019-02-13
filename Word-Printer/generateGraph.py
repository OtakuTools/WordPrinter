# -*- coding: utf-8 -*-
from graphviz import Digraph
from graphviz import Graph
import random
import os
import re
import math

class drawGraph:

    styles = {
        #'graph': {
        #    'label': 'A Fancy Graph',
        #    'fontsize': '16',
        #    'fontcolor': 'white',
        #    'bgcolor': '#333333',
        #    'rankdir': 'BT',
        #},
        'nodes': {
            'fontname': 'KaiTi',
            'shape': 'box',
            #'fontcolor': 'white',
            #'color': 'white',
            #'style': 'filled',
            #'fillcolor': '#006699',
        },
        #'edges': {
        #    'style': 'dashed',
        #    'color': 'white',
        #    'arrowhead': 'open',
        #    'fontname': 'Courier',
        #    'fontsize': '12',
        #    'fontcolor': 'white',
        #}
    }

    saveDir = "./save/"

    def __init__(self):
        pass

    def __del__(self):
        pass

    def preview(self, graph):
        graph.view()

    def save(self, graph, filename):
        graph.render(filename=self.saveDir+filename)

    def genName(self):
        s = "0123456789abcdefghijklmnopqrstuvwxyz"
        res = ""
        for i in range(32):
            res = res + s[random.randint(0, len(s)-1)]
        return res

    def apply_styles(self, graph):
        graph.graph_attr.update(
            ('graph' in self.styles and self.styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in self.styles and self.styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in self.styles and self.styles['edges']) or {}
        )
        return graph
    # gramma
    # A-B;
    # @param: data(string)
    def draw(self, data):
        edgeList = []
        nodeDict = {}
        structDict = {}
        # deal with data
        temp = data.splitlines()
        subCount = 0
        for item in temp:
            if (";" in item or "；" in item) and "#" not in item:
                s_item = item.strip(" ")
                temp_list = re.split("[;；]", s_item)
                temp_list = list(filter(lambda x: x != '' and x != ' ', temp_list))
                for item_t in temp_list:
                    edge = item_t.replace(";","").replace("；","")
                    t = re.split("[,，]", edge)
                    t = sorted(set(t), key = t.index)
                    for i in range(len(t)):
                        t[i] = t[i].strip(" ")
                    structDict["cluster{:0>5d}".format(subCount)] = t
                    subCount += 1;
            elif "#" in item and ";" not in item and "；" not in item:
                temp_list1 = re.split("[#]", item)
                for item_t in temp_list1:
                    edge = item.replace("#","")
                    edgeList.append(edge)
            else:
                return ""
        edgeList = list(filter(lambda x: x != '', edgeList))

        print(structDict)

        #print(nodeDict)
        # draw graph
        subG = []
        linkPoint = []
        graph = Graph(comment="graph", format="png", graph_attr={'rank': 'max'})
        graph.attr(_attributes={'compound': 'true', 'rankdir': 'TB', 'center': 'true'})
        for sub, content in structDict.items():
            subg = Graph(name=sub, graph_attr={'center': 'true', 'rankdir': 'LR', 'rank': 'max', 'ordering':'out'}, node_attr={'fontname': 'KaiTi', 'shape': 'box'})
            subg.attr(_attributes={'compound': 'true', 'color':'black'})
            nodes = []
            for i in range(len(content)-1, -1, -1):
                subg.node(content[i], content[i])
                nodes.append(content[i])

                if len(content)%2 == 0 and i == len(content)/2:
                    subg.node(sub+"e", "", {'height': '0', 'width':'0', 'color':'white'})
                    linkPoint.append(sub+"e")
                    nodes.append(sub+"e")
                if len(content)%2 == 1 and i == (len(content)-1)/2:
                    linkPoint.append(content[i])
                
            #for i in range(1, len(nodes)):
                #subg.edge(nodes[i-1], nodes[i])
            graph.subgraph(subg)
            subG.append(sub)

        for i in range(1, len(subG)):
            graph.edge(linkPoint[i-1], linkPoint[i], _attributes={'ltail':subG[i-1],'lhead':subG[i]})

         # single arrow
        for edge in edgeList:
            nodes = edge.split("-")
            node1 = nodes[0].strip(" ")
            node2 = nodes[1].strip(" ")
            if node1 in nodeDict:
                nodeDict[node1].append(node2)
            else:
                nodeDict[node1] = [node2]

        for node, children in nodeDict.items():
            for child in children:
                graph.edge(node, child)

        print(graph.source)
        self.preview(graph)
        filename = self.genName()
        self.save(graph, filename)
        return self.saveDir + filename + ".png"


    def testDraw(self):
        dot = Digraph(comment="Thre round Table", format="png")
        dot.node('A', "中文")
        dot.node('B', 'Knight')
        dot.node('C', 'Solider')
        dot.edges(['AB','AC'])
        dot = self.apply_styles(dot)
        print(dot.source)
        self.preview(dot)