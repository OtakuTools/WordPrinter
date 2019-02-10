# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from test import Ui_MainWindow
from database import DB
from generateGraph import drawGraph
from Word_Printer import docWriter

if __name__ == '__main__':
    #db = DB()
    graph = drawGraph()
    s = "总经理；\n\
         信息技术服务小组,管理者代表; \n\
         软件研发中心,系统集成中心,客户服务中心,营销管理中心,行政中心,财务部;\n"
    graph.draw(s)

    docw = docWriter()
    docw.write()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
sys.exit(app.exec_())