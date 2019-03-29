# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generateDocConfirm.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GenerateDocConfirm(object):
    def setupUi(self, GenerateDocConfirm):
        GenerateDocConfirm.setObjectName("GenerateDocConfirm")
        GenerateDocConfirm.resize(733, 390)
        self.showSamples = QtWidgets.QTreeWidget(GenerateDocConfirm)
        self.showSamples.setGeometry(QtCore.QRect(30, 20, 671, 321))
        self.showSamples.setObjectName("showSamples")
        self.showSamples.header().setVisible(False)
        self.DocConfirmButton = QtWidgets.QPushButton(GenerateDocConfirm)
        self.DocConfirmButton.setGeometry(QtCore.QRect(630, 350, 75, 23))
        self.DocConfirmButton.setObjectName("DocConfirmButton")

        self.retranslateUi(GenerateDocConfirm)
        QtCore.QMetaObject.connectSlotsByName(GenerateDocConfirm)

    def retranslateUi(self, GenerateDocConfirm):
        _translate = QtCore.QCoreApplication.translate
        GenerateDocConfirm.setWindowTitle(_translate("GenerateDocConfirm", "生成文档选择"))
        self.DocConfirmButton.setText(_translate("GenerateDocConfirm", "Confirm"))

