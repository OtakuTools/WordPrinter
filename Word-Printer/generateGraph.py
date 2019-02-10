# -*- coding: utf-8 -*-
from graphviz import Digraph

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
            'fontcolor': 'white',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#006699',
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

    def __init__(self):
        pass

    def __del__(self):
        pass

    def preview(self, graph):
        graph.view()

    def save(self, graph):
        graph.render(filename="./result.gv", view=True)

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

    def draw(self, data):
        pass

    def testDraw(self):
        dot = Digraph(comment="Thre round Table", format="png")
        dot.node('A', "中文")
        dot.node('B', 'Knight')
        dot.node('C', 'Solider')
        dot.edges(['AB','AC'])
        dot = self.apply_styles(dot)
        print(dot.source)
        self.preview(dot)