# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from test import Ui_MainWindow
from database import DB
from generateGraph import drawGraph
from Word_Printer import docWriter
from dataStruct import userInfo

if __name__ == '__main__':
    db = DB()

    user = userInfo();
    user.fileName = 'ABMM'
    user.company = '黄铸韬无限公司'
    user.address = '广州市最高的那栋楼'
    user.introduction = ['abm御用公司，简介还用写？？？']
    user.coverField = ['美利坚合众国的一切']
    user.manager = '狗腿1号郑经理'
    user.guandai = '狗腿2号黄管代'
    user.employees = '编制人员旭某人'
    user.approver = '批准人东某人'
    user.releaseDate = '8102年3月22日'
    user.auditDate = '9102年5月8日'
    user.picPath = 'Graph.gv.png'
    user.departments = [["aaa", ["hello", "world"], ["0", "1"]]]

    db.insertData(user)
    print(db.update("info", {"company" : "a", "address" : "b", "id" : "ABMM"}))

    #graph = drawGraph()
    #s = "总经理；\n\
    #     信息技术服务小组,管理者代表;  \n\
    #     软件研发中心,系统集成中心,客户服务中心,营销管理中心,行政中心,财务部;\n"
         #管理者代表-系统集成中心#\n\
         #信息技术服务小组-客户服务中心#"
    #graph.draw(s)

    #docw = docWriter()
    #docw.write()

    #app = QApplication(sys.argv)
    #MainWindow = QMainWindow()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
#sys.exit(app.exec_())