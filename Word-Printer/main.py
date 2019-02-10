# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from test import Ui_MainWindow
from database import DB
from generateGraph import drawGraph
from Word_Printer import docWriter

if __name__ == '__main__':
    db = DB()
    graph = drawGraph()
    docw = docWriter()

    graph.testDraw()

    docw.write()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
sys.exit(app.exec_())