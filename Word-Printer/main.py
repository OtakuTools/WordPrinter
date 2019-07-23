# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import json

from MainUI import Ui_MainWindow
from database import DB
from generateGraph import drawGraph
from Word_Printer import docWriter
from dataStruct import userInfo
from UIfunc import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controller()
    window.show()
    window.init_DB_user()

sys.exit(app.exec_())