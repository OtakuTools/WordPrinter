# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'databaseSetting.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_databaseSetting(object):
    def setupUi(self, databaseSetting):
        databaseSetting.setObjectName("databaseSetting")
        databaseSetting.resize(252, 235)
        self.gridLayout = QtWidgets.QGridLayout(databaseSetting)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(databaseSetting)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dbIP = QtWidgets.QLineEdit(databaseSetting)
        self.dbIP.setObjectName("dbIP")
        self.gridLayout.addWidget(self.dbIP, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(databaseSetting)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dbNAME = QtWidgets.QLineEdit(databaseSetting)
        self.dbNAME.setObjectName("dbNAME")
        self.gridLayout.addWidget(self.dbNAME, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(databaseSetting)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.dbUSER = QtWidgets.QLineEdit(databaseSetting)
        self.dbUSER.setObjectName("dbUSER")
        self.gridLayout.addWidget(self.dbUSER, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(databaseSetting)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.dbPSWD = QtWidgets.QLineEdit(databaseSetting)
        self.dbPSWD.setObjectName("dbPSWD")
        self.gridLayout.addWidget(self.dbPSWD, 3, 1, 1, 1)
        self.dbbuttonBox = QtWidgets.QDialogButtonBox(databaseSetting)
        self.dbbuttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dbbuttonBox.setCenterButtons(False)
        self.dbbuttonBox.setObjectName("dbbuttonBox")
        self.gridLayout.addWidget(self.dbbuttonBox, 4, 1, 1, 1)

        self.retranslateUi(databaseSetting)
        QtCore.QMetaObject.connectSlotsByName(databaseSetting)

    def retranslateUi(self, databaseSetting):
        _translate = QtCore.QCoreApplication.translate
        databaseSetting.setWindowTitle(_translate("databaseSetting", "数据库设置"))
        self.label.setText(_translate("databaseSetting", "数据库IP地址"))
        self.label_2.setText(_translate("databaseSetting", "数据库名称"))
        self.label_3.setText(_translate("databaseSetting", "用户名"))
        self.label_4.setText(_translate("databaseSetting", "密码"))

