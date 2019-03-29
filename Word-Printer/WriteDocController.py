from test import Ui_MainWindow
from generateDocConfirm import Ui_GenerateDocConfirm
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QColorDialog, QMessageBox, QCompleter, QProgressDialog 
from PyQt5.QtCore import QDate, QThread, Qt
from PyQt5.QtGui import *
import json, time, re, os, shutil
import threading

from pathSelection import pathSelection

class WriteDocController(QDialog, Ui_GenerateDocConfirm):
    
    translate = {
        "Level1" : "一层文件",
        "Level2" : "二层文件",
        "Level3" : "三层文件",
        "Level4" : "四层文件",
    }

    selectedItem = set()

    def __init__(self, fileName):
        QDialog.__init__(self)
        Ui_GenerateDocConfirm.__init__(self)
        self.setupUi(self)
        self.setConnect()
        self.pathSelector = pathSelection()

        self.setupSample(fileName)

    def setConnect(self):
        self.DocConfirmButton.clicked.connect(lambda: self.closeWindow())
        self.showSamples.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.showSamples.itemChanged.connect(self.handleChanged)

    def closeWindow(self):
        self.close()

    def setupSample(self, fileName):
        level = self.pathSelector.getLevelDir()
        tree = {}
        for key,value in level.items():
            if value in tree:
                tree[value].append(key)
            else:
                tree[value] = [key]
        
        root = QTreeWidgetItem(self.showSamples)
        root.setText(0, '模板目录')  # 设置根节点的名称
        self.showSamples.addTopLevelItem(root)

        for key,value in tree.items():
            child = QTreeWidgetItem(root)
            child.setText(0, self.translate[key])
            #child.setCheckState(0, Qt.Checked);
            for val in value:
                subchild = QTreeWidgetItem(child)
                subchild.setText(0, self.pathSelector.getFilePath(val, fileName, False))
                subchild.setCheckState(0, Qt.Checked);
    
    def handleChanged(self, item, column):
        reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})"
        prefix = re.search(reg, item.text(column), re.M|re.I)
        label = []
        if(prefix):
            label = prefix.group(1).split("-")
            label = label[-3:len(label)]
        if item.checkState(column) == Qt.Checked:
            self.selectedItem.add("-".join(label))
        elif item.checkState(column) == Qt.Unchecked:
            self.selectedItem.discard("-".join(label))
            
    def getAllSelectedFile(self):
        return self.selectedItem

class WrtDocThread(QThread):
    
    def __init__(self, user, sample, style):
        super(WrtDocThread, self).__init__()
        self.user = user
        self.sample = sample
        self.style = style

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        start_time = time.time()
        docWrt = docWriter()
        docWrt.loadAndWrite(self.user, self.sample, self.style)
        end_time = time.time()
        print("共耗时：",end_time-start_time,"秒")
        