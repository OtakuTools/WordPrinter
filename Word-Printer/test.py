# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1013, 757)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(30, 30, 971, 681))
        self.tabWidget.setObjectName("tabWidget")
        self.companyTab = QtWidgets.QWidget()
        self.companyTab.setObjectName("companyTab")
        self.basicInfo = QtWidgets.QGroupBox(self.companyTab)
        self.basicInfo.setGeometry(QtCore.QRect(10, 10, 431, 641))
        self.basicInfo.setObjectName("basicInfo")
        self.introductionText = QtWidgets.QPlainTextEdit(self.basicInfo)
        self.introductionText.setGeometry(QtCore.QRect(40, 260, 361, 361))
        self.introductionText.setObjectName("introductionText")
        self.coverFieldText = QtWidgets.QLineEdit(self.basicInfo)
        self.coverFieldText.setGeometry(QtCore.QRect(110, 150, 291, 20))
        self.coverFieldText.setObjectName("coverFieldText")
        self.coverFieldLable = QtWidgets.QLabel(self.basicInfo)
        self.coverFieldLable.setGeometry(QtCore.QRect(40, 150, 61, 20))
        self.coverFieldLable.setObjectName("coverFieldLable")
        self.fileNameLable = QtWidgets.QLabel(self.basicInfo)
        self.fileNameLable.setGeometry(QtCore.QRect(40, 30, 54, 12))
        self.fileNameLable.setObjectName("fileNameLable")
        self.fileNameText = QtWidgets.QLineEdit(self.basicInfo)
        self.fileNameText.setGeometry(QtCore.QRect(110, 30, 291, 20))
        self.fileNameText.setObjectName("fileNameText")
        self.companyLable = QtWidgets.QLabel(self.basicInfo)
        self.companyLable.setGeometry(QtCore.QRect(40, 70, 54, 12))
        self.companyLable.setObjectName("companyLable")
        self.companyText = QtWidgets.QLineEdit(self.basicInfo)
        self.companyText.setGeometry(QtCore.QRect(110, 70, 291, 20))
        self.companyText.setObjectName("companyText")
        self.addressLable = QtWidgets.QLabel(self.basicInfo)
        self.addressLable.setGeometry(QtCore.QRect(40, 110, 54, 12))
        self.addressLable.setObjectName("addressLable")
        self.addressText = QtWidgets.QLineEdit(self.basicInfo)
        self.addressText.setGeometry(QtCore.QRect(110, 110, 291, 20))
        self.addressText.setObjectName("addressText")
        self.introductionLable = QtWidgets.QLabel(self.basicInfo)
        self.introductionLable.setGeometry(QtCore.QRect(40, 230, 81, 16))
        self.introductionLable.setObjectName("introductionLable")
        self.policyText = QtWidgets.QLineEdit(self.basicInfo)
        self.policyText.setGeometry(QtCore.QRect(110, 200, 291, 20))
        self.policyText.setObjectName("policyText")
        self.policyLable = QtWidgets.QLabel(self.basicInfo)
        self.policyLable.setGeometry(QtCore.QRect(40, 200, 54, 12))
        self.policyLable.setObjectName("policyLable")
        self.fileInfo = QtWidgets.QGroupBox(self.companyTab)
        self.fileInfo.setGeometry(QtCore.QRect(490, 10, 461, 641))
        self.fileInfo.setObjectName("fileInfo")
        self.auditDateText = QtWidgets.QDateEdit(self.fileInfo)
        self.auditDateText.setGeometry(QtCore.QRect(80, 300, 110, 22))
        self.auditDateText.setObjectName("auditDateText")
        self.zipText = QtWidgets.QLineEdit(self.fileInfo)
        self.zipText.setGeometry(QtCore.QRect(80, 190, 113, 20))
        self.zipText.setObjectName("zipText")
        self.modifyDateText = QtWidgets.QDateEdit(self.fileInfo)
        self.modifyDateText.setGeometry(QtCore.QRect(310, 240, 110, 22))
        self.modifyDateText.setObjectName("modifyDateText")
        self.approverText = QtWidgets.QLineEdit(self.fileInfo)
        self.approverText.setGeometry(QtCore.QRect(310, 90, 113, 20))
        self.approverText.setObjectName("approverText")
        self.announcerText = QtWidgets.QLineEdit(self.fileInfo)
        self.announcerText.setGeometry(QtCore.QRect(310, 140, 113, 20))
        self.announcerText.setObjectName("announcerText")
        self.employeesText = QtWidgets.QLineEdit(self.fileInfo)
        self.employeesText.setGeometry(QtCore.QRect(80, 90, 113, 20))
        self.employeesText.setObjectName("employeesText")
        self.managerText = QtWidgets.QLineEdit(self.fileInfo)
        self.managerText.setGeometry(QtCore.QRect(80, 40, 113, 20))
        self.managerText.setObjectName("managerText")
        self.releaseDateText = QtWidgets.QDateEdit(self.fileInfo)
        self.releaseDateText.setGeometry(QtCore.QRect(90, 240, 110, 22))
        self.releaseDateText.setObjectName("releaseDateText")
        self.phoneText = QtWidgets.QLineEdit(self.fileInfo)
        self.phoneText.setGeometry(QtCore.QRect(310, 190, 113, 20))
        self.phoneText.setObjectName("phoneText")
        self.guandaiText = QtWidgets.QLineEdit(self.fileInfo)
        self.guandaiText.setGeometry(QtCore.QRect(310, 40, 113, 20))
        self.guandaiText.setObjectName("guandaiText")
        self.auditText = QtWidgets.QLineEdit(self.fileInfo)
        self.auditText.setGeometry(QtCore.QRect(80, 140, 113, 20))
        self.auditText.setObjectName("auditText")
        self.managerLable = QtWidgets.QLabel(self.fileInfo)
        self.managerLable.setGeometry(QtCore.QRect(20, 40, 54, 12))
        self.managerLable.setObjectName("managerLable")
        self.guandaiLable = QtWidgets.QLabel(self.fileInfo)
        self.guandaiLable.setGeometry(QtCore.QRect(233, 40, 61, 20))
        self.guandaiLable.setObjectName("guandaiLable")
        self.employeesLable = QtWidgets.QLabel(self.fileInfo)
        self.employeesLable.setGeometry(QtCore.QRect(20, 90, 54, 12))
        self.employeesLable.setObjectName("employeesLable")
        self.approverLable = QtWidgets.QLabel(self.fileInfo)
        self.approverLable.setGeometry(QtCore.QRect(240, 90, 54, 12))
        self.approverLable.setObjectName("approverLable")
        self.auditLable = QtWidgets.QLabel(self.fileInfo)
        self.auditLable.setGeometry(QtCore.QRect(20, 140, 54, 12))
        self.auditLable.setObjectName("auditLable")
        self.announcerLable = QtWidgets.QLabel(self.fileInfo)
        self.announcerLable.setGeometry(QtCore.QRect(240, 140, 54, 12))
        self.announcerLable.setObjectName("announcerLable")
        self.zipLable = QtWidgets.QLabel(self.fileInfo)
        self.zipLable.setGeometry(QtCore.QRect(20, 190, 54, 12))
        self.zipLable.setObjectName("zipLable")
        self.phoneLable = QtWidgets.QLabel(self.fileInfo)
        self.phoneLable.setGeometry(QtCore.QRect(240, 190, 54, 12))
        self.phoneLable.setObjectName("phoneLable")
        self.modifyDateLable = QtWidgets.QLabel(self.fileInfo)
        self.modifyDateLable.setGeometry(QtCore.QRect(240, 240, 54, 21))
        self.modifyDateLable.setObjectName("modifyDateLable")
        self.releaseDateLable = QtWidgets.QLabel(self.fileInfo)
        self.releaseDateLable.setGeometry(QtCore.QRect(10, 240, 81, 16))
        self.releaseDateLable.setObjectName("releaseDateLable")
        self.auditDateLable = QtWidgets.QLabel(self.fileInfo)
        self.auditDateLable.setGeometry(QtCore.QRect(20, 300, 54, 12))
        self.auditDateLable.setObjectName("auditDateLable")
        self.groupBox_3 = QtWidgets.QGroupBox(self.fileInfo)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 340, 441, 291))
        self.groupBox_3.setObjectName("groupBox_3")
        self.depStructLable = QtWidgets.QLabel(self.groupBox_3)
        self.depStructLable.setGeometry(QtCore.QRect(10, 20, 54, 12))
        self.depStructLable.setObjectName("depStructLable")
        self.previewPic = QtWidgets.QTableWidget(self.groupBox_3)
        self.previewPic.setGeometry(QtCore.QRect(10, 40, 211, 231))
        self.previewPic.setObjectName("previewPic")
        self.previewPic.setColumnCount(0)
        self.previewPic.setRowCount(0)
        self.previewButton = QtWidgets.QPushButton(self.groupBox_3)
        self.previewButton.setGeometry(QtCore.QRect(360, 240, 75, 23))
        self.previewButton.setObjectName("previewButton")
        self.deSytle = QtWidgets.QLabel(self.groupBox_3)
        self.deSytle.setGeometry(QtCore.QRect(240, 20, 31, 16))
        self.deSytle.setObjectName("deSytle")
        self.level1Lable = QtWidgets.QLabel(self.groupBox_3)
        self.level1Lable.setGeometry(QtCore.QRect(240, 60, 54, 12))
        self.level1Lable.setObjectName("level1Lable")
        self.level2Lable = QtWidgets.QLabel(self.groupBox_3)
        self.level2Lable.setGeometry(QtCore.QRect(240, 100, 54, 12))
        self.level2Lable.setObjectName("level2Lable")
        self.level3Lable = QtWidgets.QLabel(self.groupBox_3)
        self.level3Lable.setGeometry(QtCore.QRect(240, 140, 54, 12))
        self.level3Lable.setObjectName("level3Lable")
        self.level4Lable = QtWidgets.QLabel(self.groupBox_3)
        self.level4Lable.setGeometry(QtCore.QRect(240, 180, 54, 12))
        self.level4Lable.setObjectName("level4Lable")
        self.borderLable = QtWidgets.QLabel(self.groupBox_3)
        self.borderLable.setGeometry(QtCore.QRect(300, 20, 31, 16))
        self.borderLable.setObjectName("borderLable")
        self.fontLable = QtWidgets.QLabel(self.groupBox_3)
        self.fontLable.setGeometry(QtCore.QRect(350, 20, 31, 16))
        self.fontLable.setObjectName("fontLable")
        self.heightLable = QtWidgets.QLabel(self.groupBox_3)
        self.heightLable.setGeometry(QtCore.QRect(400, 20, 31, 16))
        self.heightLable.setObjectName("heightLable")
        self.level1Height = QtWidgets.QSpinBox(self.groupBox_3)
        self.level1Height.setGeometry(QtCore.QRect(390, 50, 42, 22))
        self.level1Height.setObjectName("level1Height")
        self.level2Height = QtWidgets.QSpinBox(self.groupBox_3)
        self.level2Height.setGeometry(QtCore.QRect(390, 90, 42, 22))
        self.level2Height.setObjectName("level2Height")
        self.level3Height = QtWidgets.QSpinBox(self.groupBox_3)
        self.level3Height.setGeometry(QtCore.QRect(390, 130, 42, 22))
        self.level3Height.setObjectName("level3Height")
        self.level4Height = QtWidgets.QSpinBox(self.groupBox_3)
        self.level4Height.setGeometry(QtCore.QRect(390, 170, 42, 22))
        self.level4Height.setObjectName("level4Height")
        self.level1Border = QtWidgets.QPushButton(self.groupBox_3)
        self.level1Border.setGeometry(QtCore.QRect(300, 50, 21, 20))
        self.level1Border.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level1Border.setText("")
        self.level1Border.setObjectName("level1Border")
        self.level2Border = QtWidgets.QPushButton(self.groupBox_3)
        self.level2Border.setGeometry(QtCore.QRect(300, 90, 21, 20))
        self.level2Border.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level2Border.setText("")
        self.level2Border.setObjectName("level2Border")
        self.level3Border = QtWidgets.QPushButton(self.groupBox_3)
        self.level3Border.setGeometry(QtCore.QRect(300, 130, 21, 20))
        self.level3Border.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level3Border.setText("")
        self.level3Border.setObjectName("level3Border")
        self.level4Border = QtWidgets.QPushButton(self.groupBox_3)
        self.level4Border.setGeometry(QtCore.QRect(300, 170, 21, 20))
        self.level4Border.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level4Border.setText("")
        self.level4Border.setObjectName("level4Border")
        self.level1Font = QtWidgets.QPushButton(self.groupBox_3)
        self.level1Font.setGeometry(QtCore.QRect(350, 50, 21, 20))
        self.level1Font.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level1Font.setText("")
        self.level1Font.setObjectName("level1Font")
        self.level2Font = QtWidgets.QPushButton(self.groupBox_3)
        self.level2Font.setGeometry(QtCore.QRect(350, 90, 21, 20))
        self.level2Font.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level2Font.setText("")
        self.level2Font.setObjectName("level2Font")
        self.level3Font = QtWidgets.QPushButton(self.groupBox_3)
        self.level3Font.setGeometry(QtCore.QRect(350, 130, 21, 20))
        self.level3Font.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level3Font.setText("")
        self.level3Font.setObjectName("level3Font")
        self.level4Font = QtWidgets.QPushButton(self.groupBox_3)
        self.level4Font.setGeometry(QtCore.QRect(350, 170, 21, 20))
        self.level4Font.setStyleSheet("background-color:rgb(255, 255, 0);\n"
"border-color: rgb(0, 0, 0);\n"
"gridline-color:rgb(0, 0, 0);")
        self.level4Font.setText("")
        self.level4Font.setObjectName("level4Font")
        self.tabWidget.addTab(self.companyTab, "")
        self.departmentTab = QtWidgets.QWidget()
        self.departmentTab.setObjectName("departmentTab")
        self.groupBox_4 = QtWidgets.QGroupBox(self.departmentTab)
        self.groupBox_4.setGeometry(QtCore.QRect(30, 20, 351, 601))
        self.groupBox_4.setObjectName("groupBox_4")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_4)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 331, 571))
        self.listWidget.setObjectName("listWidget")
        self.groupBox_5 = QtWidgets.QGroupBox(self.departmentTab)
        self.groupBox_5.setGeometry(QtCore.QRect(440, 20, 511, 601))
        self.groupBox_5.setObjectName("groupBox_5")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.groupBox_5)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(20, 50, 471, 361))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label_27 = QtWidgets.QLabel(self.groupBox_5)
        self.label_27.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.groupBox_5)
        self.label_28.setGeometry(QtCore.QRect(20, 420, 54, 12))
        self.label_28.setObjectName("label_28")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox.setGeometry(QtCore.QRect(20, 440, 71, 16))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_2.setGeometry(QtCore.QRect(100, 440, 71, 16))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_3.setGeometry(QtCore.QRect(180, 440, 71, 16))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_4.setGeometry(QtCore.QRect(260, 440, 71, 16))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_5.setGeometry(QtCore.QRect(340, 440, 71, 16))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_6.setGeometry(QtCore.QRect(420, 440, 71, 16))
        self.checkBox_6.setObjectName("checkBox_6")
        self.tabWidget.addTab(self.departmentTab, "")
        self.createBotton = QtWidgets.QPushButton(self.centralwidget)
        self.createBotton.setGeometry(QtCore.QRect(830, 20, 75, 23))
        self.createBotton.setObjectName("createBotton")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setGeometry(QtCore.QRect(920, 20, 75, 23))
        self.cancelButton.setObjectName("cancelButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1013, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.basicInfo.setTitle(_translate("MainWindow", "基础信息"))
        self.coverFieldLable.setText(_translate("MainWindow", "业务范围"))
        self.fileNameLable.setText(_translate("MainWindow", "公司缩写"))
        self.companyLable.setText(_translate("MainWindow", "公司名"))
        self.addressLable.setText(_translate("MainWindow", "地址"))
        self.introductionLable.setText(_translate("MainWindow", "公司简介"))
        self.policyLable.setText(_translate("MainWindow", "服务方针"))
        self.fileInfo.setTitle(_translate("MainWindow", "文档信息"))
        self.managerLable.setText(_translate("MainWindow", "总经理"))
        self.guandaiLable.setText(_translate("MainWindow", "管理者代表"))
        self.employeesLable.setText(_translate("MainWindow", "编制人"))
        self.approverLable.setText(_translate("MainWindow", "批准人"))
        self.auditLable.setText(_translate("MainWindow", "审计人"))
        self.announcerLable.setText(_translate("MainWindow", "发布人"))
        self.zipLable.setText(_translate("MainWindow", "邮编"))
        self.phoneLable.setText(_translate("MainWindow", "电话"))
        self.modifyDateLable.setText(_translate("MainWindow", "修改日期"))
        self.releaseDateLable.setText(_translate("MainWindow", "发布批准日期"))
        self.auditDateLable.setText(_translate("MainWindow", "审计日期"))
        self.groupBox_3.setTitle(_translate("MainWindow", "结构图"))
        self.depStructLable.setText(_translate("MainWindow", "部门结构"))
        self.previewButton.setText(_translate("MainWindow", "预览图片"))
        self.deSytle.setText(_translate("MainWindow", "样式"))
        self.level1Lable.setText(_translate("MainWindow", "第一层"))
        self.level2Lable.setText(_translate("MainWindow", "第二层"))
        self.level3Lable.setText(_translate("MainWindow", "第三层"))
        self.level4Lable.setText(_translate("MainWindow", "第四层"))
        self.borderLable.setText(_translate("MainWindow", "边框"))
        self.fontLable.setText(_translate("MainWindow", "字体"))
        self.heightLable.setText(_translate("MainWindow", "行宽"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.companyTab), _translate("MainWindow", "公司信息"))
        self.groupBox_4.setTitle(_translate("MainWindow", "部门列表"))
        self.groupBox_5.setTitle(_translate("MainWindow", "部门信息"))
        self.label_27.setText(_translate("MainWindow", "部门简介"))
        self.label_28.setText(_translate("MainWindow", "部门职责"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_3.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_4.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_5.setText(_translate("MainWindow", "CheckBox"))
        self.checkBox_6.setText(_translate("MainWindow", "CheckBox"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.departmentTab), _translate("MainWindow", "部门信息"))
        self.createBotton.setText(_translate("MainWindow", "生成"))
        self.cancelButton.setText(_translate("MainWindow", "取消"))

