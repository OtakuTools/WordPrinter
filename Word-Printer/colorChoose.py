# -*- coding: utf-8 -*-
# 生成前必须将下列代码保存，否则将丢失
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QColorDialog , QWidget
from PyQt5.QtGui import QColor 
from PyQt5.QtCore import Qt 

class ColorDialog(QWidget): 
    def __init__(self ): 
        super().__init__() 
        #颜色值
        color = QColor(0, 0, 0) 
        #位置
        self.setGeometry(300, 300, 350, 280) 
        #标题
        self.setWindowTitle('颜色选择') 
        #按钮名称
        self.button = QtWidgets.QPushButton('Dialog', self) 
        self.button.setFocusPolicy(Qt.NoFocus) 
        #按钮位置
        self.button.move(40, 20) 
        #按钮绑定方法
        self.button.clicked.connect(self.showDialog) 
        self.setFocus()
        self.widget = QWidget(self) 
        self.widget.setStyleSheet('QWidget{background-color:%s} '%color.name()) 
        self.widget.setGeometry(130, 22, 200, 100) 
        
    def showDialog(self): 
        col = QColorDialog.getColor() 
        print(col.name(),"\n")
        if col.isValid(): 
            self.widget.setStyleSheet('QWidget {background-color:%s}'%col.name()) 
