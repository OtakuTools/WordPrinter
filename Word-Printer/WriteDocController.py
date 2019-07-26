from MainUI import Ui_MainWindow
from generateDocConfirm import Ui_GenerateDocConfirm
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QThread, Qt
from PyQt5.QtGui import *
import json, time, re, os, shutil
import threading

from pathSelection import pathSelection, pathSelection_v2
from Word_Printer import docWriter

class WriteDocController(QDialog, Ui_GenerateDocConfirm):
    
    translate = {
        "Level1" : "一层文件",
        "Level2" : "二层文件",
        "Level3" : "三层文件",
        "Level4" : "四层文件",
    }

    selectedItem = set()

    def __init__(self, fileName, selectedFile = None):
        QDialog.__init__(self)
        Ui_GenerateDocConfirm.__init__(self)
        self.setupUi(self)
        self.setConnect()
        self.pathSelector = pathSelection()
        self.pathSelector_v2 = pathSelection_v2()

        #self.setupSample(fileName, selectedFile)
        self.setupSample_v2("Company", ["project1", "project2"], selectedFile)

    def setConnect(self):
        self.confirmBox.accepted.connect(lambda: self.confirm())
        self.confirmBox.rejected.connect(lambda: self.cancel())
        self.showSamples.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.showSamples.itemChanged.connect(self.handleChanged_v2)

    def confirm(self):
        self.accept()

    def cancel(self):
        self.reject()

    def setupSample_v2(self, fileName, projects, selectedFile):
        try:
            self.pathSelector_v2.autoRefresh(fileName, projects)
            self.showSamples.setAnimated(True)
            self.setupTreeView(self.pathSelector_v2.customFileTree, self.pathSelector_v2.sampleDir, None, selectedFile)
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
                    if p in selectedFile:
                        child.setCheckState(0, Qt.Checked)
                    else:
                        child.setCheckState(0, Qt.Unchecked)
                else:
                    self.setupTreeView(treeNode[k], k, child, selectedFile, isRoot, p)

    def setupSample(self, fileName, selectedFile):
        level = self.pathSelector.getLevelDir()
        tree = {}
        for key,value in level.items():
            if value in tree:
                tree[value].append(key)
            else:
                tree[value] = [key]

        self.showSamples.setAnimated(True)
        root = QTreeWidgetItem(self.showSamples)
        root.setText(0, '模板目录')  # 设置根节点的名称
        self.showSamples.addTopLevelItem(root)

        for key,value in tree.items():
            child = QTreeWidgetItem(root)
            child.setText(0, self.translate[key])
            for val in value:
                fPath = os.path.split(self.pathSelector.getFilePath(val, fileName, False))
                prefix = fPath[0].split("\\")[-1]
                if prefix == key:
                    subchild = QTreeWidgetItem(child)
                    subchild.setText(0, fPath[1])
                    if val in selectedFile:
                        subchild.setCheckState(0, Qt.Checked)
                    else:
                        subchild.setCheckState(0, Qt.Unchecked)
                else:
                    subchild_vec = self.showSamples.findItems(prefix, Qt.MatchExactly | Qt.MatchRecursive, 0)
                    if len(subchild_vec) == 0:
                        subchild = QTreeWidgetItem(child)
                        subchild.setText(0, prefix)
                    else:
                        subchild = subchild_vec[0]
                    subsubchild = QTreeWidgetItem(subchild)
                    subsubchild.setText(0, fPath[1])
                    if val in selectedFile:
                        subsubchild.setCheckState(0, Qt.Checked)
                    else:
                        subsubchild.setCheckState(0, Qt.Unchecked)
        self.showSamples.expandItem(root)
        #self.showSamples.expandAll()
    
    def handleChanged(self, item, column):
        reg = "([A-Z]{4}-\d{5}-[A-Z]{2}-[A-Z]-\d{2})(.*)(.docx|.doc|.xls|.xlsx)"
        prefix = re.search(reg, item.text(column), re.M|re.I)
        label = []
        if(prefix):
            label = prefix.group(1).split("-")
            label = label[-3:len(label)]
        print(item.text(column+1))
        if item.checkState(column) == Qt.Checked:
            self.selectedItem.add("-".join(label))
        elif item.checkState(column) == Qt.Unchecked:
            self.selectedItem.discard("-".join(label))

    def handleChanged_v2(self, item, column):
        if item.text(column+1):
            print(self.pathSelector_v2.getFileInfo(item.text(column+1)))
        if item.checkState(column) == Qt.Checked:
            if item.text(column+1):
                self.selectedItem.add(item.text(column+1))
        elif item.checkState(column) == Qt.Unchecked:
            if item.text(column+1):
                self.selectedItem.discard(item.text(column+1))
            
    def getAllSelectedFile(self):
        return self.selectedItem

class WrtDocThread(QThread):
    
    def __init__(self, user, sample, style, target):
        super(WrtDocThread, self).__init__()
        self.user = user
        self.sample = sample
        self.style = style
        self.target = target

    def __del__(self):
        self.quit()
        self.wait()

    def run(self):
        start_time = time.time()
        docWrt = docWriter()
        docWrt.loadAndWrite(self.user, self.sample, self.style, self.target)
        end_time = time.time()
        print("共耗时：",end_time-start_time,"秒")
        