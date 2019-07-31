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
        self.gridLayout = QtWidgets.QGridLayout(GenerateDocConfirm)
        self.gridLayout.setObjectName("gridLayout")
        self.showSamples = QtWidgets.QTreeWidget(GenerateDocConfirm)
        self.showSamples.setObjectName("showSamples")
        self.showSamples.headerItem().setText(0, "1")
        self.showSamples.header().setVisible(False)
        self.gridLayout.addWidget(self.showSamples, 0, 0, 1, 1)
        self.confirmBox = QtWidgets.QDialogButtonBox(GenerateDocConfirm)
        self.confirmBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirmBox.setObjectName("confirmBox")
        self.gridLayout.addWidget(self.confirmBox, 1, 0, 1, 1)

        self.retranslateUi(GenerateDocConfirm)
        QtCore.QMetaObject.connectSlotsByName(GenerateDocConfirm)

    def retranslateUi(self, GenerateDocConfirm):
        _translate = QtCore.QCoreApplication.translate
        GenerateDocConfirm.setWindowTitle(_translate("GenerateDocConfirm", "生成文档选择"))
        GenerateDocConfirm.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint |
                               QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint |
                               QtCore.Qt.WindowStaysOnTopHint)

