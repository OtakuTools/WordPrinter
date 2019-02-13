# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import json

from test import Ui_MainWindow
from database import DB
from generateGraph import drawGraph
from Word_Printer import docWriter
from dataStruct import userInfo

if __name__ == '__main__':
    db = DB()

    user = userInfo();
    with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
    dict = data[0]
    for key in dict.keys():
        setattr( user , key , dict[key] )

    
    #db.insertData(user)
    #print(db.update("info", {"company" : "a", "address" : "b", "id" : "ABMM"}))
    #print(db.update("department", {"name" : "aaa", "resposibility" : ["3","4"], "refId" : "ABMM"}))
    #print(db.delete("department", "ABMM", "aaa") )

    #graph = drawGraph()
    #s = "总经理；\n\
    #     信息技术服务小组,管理者代表;  \n\
    #     软件研发中心,系统集成中心,客户服务中心,营销管理中心,行政中心,财务部;\n"
         #管理者代表-系统集成中心#\n\
         #信息技术服务小组-客户服务中心#"
    #graph.draw(s)

    docw = docWriter()
    docw.loadAndWrite("sample.docx")

    #app = QApplication(sys.argv)
    #MainWindow = QMainWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
#sys.exit(app.exec_())