# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import json

from test import Ui_MainWindow
from colorChoose import ColorDialog
from database import DB
from generateGraph import drawGraph
from Word_Printer import docWriter
from dataStruct import userInfo
from UIfunc import Controller

if __name__ == '__main__':
    db = DB()

    user = userInfo();
    with open("TestCase.json", "r" , encoding='utf-8') as f:
            data = json.load(f)
    for dict in data:
        for key in dict.keys():
            setattr( user , key , dict[key] )
        db.insertData(user)

    db.searchById("广州真如信息科技有限公司")
    print(db.update("info", {"company" : "广州真如信息科技有限公司", "address" : "b", "id" : "asdasdasd"}))
    #print(db.update("department", {"name" : "客户服务中心", "intro":["hello", "world"], "func" : [3,4], "refId" : "广州真如信息科技有限公司"}))
    #print(db.delete("department", "ABMM", "aaa") )

    #app = QApplication(sys.argv)
    #window = Controller()
    #window.show()
    #sys.exit(app.exec_())