# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WordPad.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WordPad(object):
    def setupUi(self, WordPad):
        WordPad.setObjectName("WordPad")
        WordPad.resize(606, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(WordPad.sizePolicy().hasHeightForWidth())
        WordPad.setSizePolicy(sizePolicy)
        WordPad.setSizeIncrement(QtCore.QSize(-1, 1))
        WordPad.setAutoFillBackground(False)
        WordPad.setSizeGripEnabled(False)
        self.gridLayout = QtWidgets.QGridLayout(WordPad)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(WordPad)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.wp_comfirmButton = QtWidgets.QDialogButtonBox(WordPad)
        self.wp_comfirmButton.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.wp_comfirmButton.setCenterButtons(False)
        self.wp_comfirmButton.setObjectName("wp_comfirmButton")
        self.gridLayout.addWidget(self.wp_comfirmButton, 0, 7, 1, 1)
        self.wp_fontSize = QtWidgets.QSpinBox(WordPad)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wp_fontSize.sizePolicy().hasHeightForWidth())
        self.wp_fontSize.setSizePolicy(sizePolicy)
        self.wp_fontSize.setMinimum(10)
        self.wp_fontSize.setObjectName("wp_fontSize")
        self.gridLayout.addWidget(self.wp_fontSize, 0, 4, 1, 1)
        self.FontSize = QtWidgets.QLabel(WordPad)
        self.FontSize.setObjectName("FontSize")
        self.gridLayout.addWidget(self.FontSize, 0, 3, 1, 1)
        self.wp_fontType = QtWidgets.QFontComboBox(WordPad)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wp_fontType.sizePolicy().hasHeightForWidth())
        self.wp_fontType.setSizePolicy(sizePolicy)
        self.wp_fontType.setObjectName("wp_fontType")
        self.gridLayout.addWidget(self.wp_fontType, 0, 2, 1, 1)
        self.wp_textContent = QtWidgets.QPlainTextEdit(WordPad)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.wp_textContent.setFont(font)
        self.wp_textContent.setObjectName("wp_textContent")
        self.gridLayout.addWidget(self.wp_textContent, 1, 0, 1, 8)

        self.retranslateUi(WordPad)
        QtCore.QMetaObject.connectSlotsByName(WordPad)

    def retranslateUi(self, WordPad):
        _translate = QtCore.QCoreApplication.translate
        WordPad.setWindowTitle(_translate("WordPad", "写字板"))
        WordPad.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint |
                               QtCore.Qt.WindowMinimizeButtonHint |
                               QtCore.Qt.WindowCloseButtonHint |
                               QtCore.Qt.WindowStaysOnTopHint)
        self.label.setText(_translate("WordPad", "字体样式"))
        self.FontSize.setText(_translate("WordPad", "字体大小"))

