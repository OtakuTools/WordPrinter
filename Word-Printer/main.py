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
    user.fileName = 'SAMP'
    user.company = '很有钱有限公司'
    user.address = '广州市某区某街道某楼某层某号'
    user.introduction = ['这里是简介','最多只有800字','简介简介简介简介简介简介简介简介简介简介']
    user.coverField = ['这里是管理经营范围','最多不知道多少字','也不知道能不能换行','经营范围经营范围经营范围经营范围']
    user.manager = '经理名字某某某'
    user.guandai = '管代名字某某某'
    user.employees = '编制人员姓名某某人'
    user.approver = '批准发布人某某人'
    user.releaseDate = '8102年1月31日'
    user.auditDate = '9102年2月28日'
    user.picPath = 'Graph.gv.png'
    user.departments = [{'name':'很有钱的软件开发部','intro':['开','发','软','件']},{'name':'很有钱的客服','intro':['聊','天','系统集成中心是公司的直接创利部门之一，进行系统集成方面的业务开拓，实现公司要求的年度经营目标；']}]

    db.insertData(user)
    #print(db.update("info", {"company" : "a", "address" : "b", "id" : "ABMM"}))
    print(db.update("department", {"name" : "aaa", "resposibility" : ["3","4"], "refId" : "ABMM"}))
    #print(db.delete("department", "ABMM", "aaa") )

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