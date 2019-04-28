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
        self.showSamples.headerItem().setText(0, "1")
        self.showSamples.header().setVisible(False)
        self.confirmBox = QtWidgets.QDialogButtonBox(GenerateDocConfirm)
        self.confirmBox.setGeometry(QtCore.QRect(550, 350, 156, 23))
        self.confirmBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirmBox.setObjectName("confirmBox")

        self.retranslateUi(GenerateDocConfirm)
        QtCore.QMetaObject.connectSlotsByName(GenerateDocConfirm)

    def retranslateUi(self, GenerateDocConfirm):
        _translate = QtCore.QCoreApplication.translate
        GenerateDocConfirm.setWindowTitle(_translate("GenerateDocConfirm", "生成文档选择"))

