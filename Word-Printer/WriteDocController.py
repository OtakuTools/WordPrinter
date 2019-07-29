from MainUI import Ui_MainWindow
from generateDocConfirm import Ui_GenerateDocConfirm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QThread, Qt
from PyQt5.QtGui import *
import json, time, re, os, shutil
import threading

from pathSelection import pathSelection
from Word_Printer import docWriter

class WriteDocController(QDialog, Ui_GenerateDocConfirm):
    
    translate = {
        "Level1" : "一层文件",
        "Level2" : "二层文件",
        "Level3" : "三层文件",
        "Level4" : "四层文件",
    }

    version = "2.0.0"

    def __init__(self, fileName, projects=None, selectedFile = None):
        QDialog.__init__(self)
        Ui_GenerateDocConfirm.__init__(self)
        self.selectedItem = set()
        self.setupUi(self)
        self.setConnect()
        self.pathSelector = pathSelection()
        self.setupSample(fileName, projects, selectedFile)

    def setConnect(self):
        self.confirmBox.accepted.connect(lambda: self.confirm())
        self.confirmBox.rejected.connect(lambda: self.cancel())
        self.showSamples.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.showSamples.itemChanged.connect(self.handleChanged)

    def confirm(self):
        self.accept()

    def cancel(self):
        self.reject()

    def setupSample(self, fileName, projects, selectedFile):
        try:
            self.pathSelector.autoRefresh(fileName, projects)
            self.showSamples.setAnimated(True)
            self.setupTreeView(self.pathSelector.customFileTree, self.pathSelector.sampleDir, None, selectedFile)
        except Exception as e:
            print(e)
        

    def setupTreeView(self, treeNode, nodeName, viewNode, selectedFile, isRoot=True, filePath=None):
        if isRoot:
            isRoot = False
            root = QTreeWidgetItem(self.showSamples)
            root.setText(0, '模板目录')  # 设置根节点的名称
            self.showSamples.addTopLevelItem(root)
            self.setupTreeView(treeNode[nodeName], None, root, selectedFile, isRoot, nodeName)
            self.showSamples.expandItem(root)
            return
        if isinstance(treeNode, list):
            return
        else:
            for k, v in treeNode.items():
                p = "/".join([filePath, k])
                child = QTreeWidgetItem(viewNode)
                if k in self.translate:
                    child.setText(0, self.translate[k])
                else:
                    child.setText(0, k)
                child.setText(1, p)
                if isinstance(treeNode[k], list):
                    child.setText(2, "0")
                    if p in selectedFile:
                        child.setCheckState(0, Qt.Checked)
                    else:
                        child.setCheckState(0, Qt.Unchecked)
                else:
                    child.setText(2, "1")
                    child.setCheckState(0, Qt.Unchecked)
                    self.setupTreeView(treeNode[k], k, child, selectedFile, isRoot, p)

    def changeChildStatus(self, node, status):
        if not node:
            return
        for i in range(node.childCount()):
            node_i = node.child(i)
            node_i.setCheckState(0, status)
            self.changeChildStatus(node_i, status)
    
    def changeParentStatus(self, node):
        if not node:
            return
        parent = node.parent()
        selectCount = 0
        cancelCount = 0
        status = Qt.Checked
        for i in range(parent.childCount()):
            if parent.child(i).checkState(0) == Qt.Unchecked:
                cancelCount += 1
            else:
                selectCount += 1
        if selectCount == parent.childCount():
            status = Qt.Checked
        elif cancelCount == parent.childCount():
            status = Qt.Unchecked
        else:
            status = Qt.PartiallyChecked
        parent.setCheckState(0, status)

    def handleChanged(self, item, column):
        if item.checkState(column) == Qt.Checked:
            if item.text(column+1) and item.text(column+2) and item.text(column+2) == "0":
                self.selectedItem.add(item.text(column+1))
                self.changeParentStatus(item)
            elif item.text(column+2) and item.text(column+2) == "1":
                self.changeChildStatus(item, Qt.Checked)
        elif item.checkState(column) == Qt.Unchecked:
            if item.text(column+1) and item.text(column+2) and item.text(column+2) == "0":
                self.selectedItem.discard(item.text(column+1))
                self.changeParentStatus(item)
            elif item.text(column+2) and item.text(column+2) == "1":
                self.changeChildStatus(item, Qt.Unchecked)

    def getAllSelectedFile(self):
        return self.selectedItem

class WrtDocThread(QThread):
    
    def __init__(self, user, srcDir, tarDir, fileType):
        super(WrtDocThread, self).__init__()
        self.user = user
        self.sample = srcDir
        self.target = tarDir
        self.type = fileType

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        start_time = time.time()
        docWrt = docWriter()
        docWrt.loadAndWrite(self.user, self.sample, self.target, self.type)
        end_time = time.time()
        print("共耗时：",end_time-start_time,"秒")
        