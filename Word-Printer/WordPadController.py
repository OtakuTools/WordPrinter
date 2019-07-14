from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, QThread, Qt
from PyQt5.QtGui import *

from WordPad import Ui_WordPad

class WordPadController(QDialog, Ui_WordPad):

    def __init__(self, input=""):
        QDialog.__init__(self)
        Ui_WordPad.__init__(self)
        self.setupUi(self)
        self.setConnection()
        self.initInfo(input)

    def setConnection(self):
        self.wp_fontType.currentFontChanged.connect(self.fontTypeHandler)
        self.wp_fontSize.valueChanged.connect(self.fontSizeHandler)
        self.wp_comfirmButton.accepted.connect(self.save)
        self.wp_comfirmButton.rejected.connect(self.cancel)
        self.wp_textContent.textChanged.connect(self.textHandler)

    def textHandler(self):
        self.finalText = self.wp_textContent.toPlainText()

    def fontTypeHandler(self):
        #print(self.wp_fontType.currentFont().family())
        self.setFontStyle()

    def fontSizeHandler(self):
        #print(self.wp_fontSize.value())
        self.setFontStyle()

    def setFontStyle(self):
        font = QFont()
        font.setFamily(self.wp_fontType.currentFont().family())
        font.setPointSize(self.wp_fontSize.value())
        self.wp_textContent.setFont(font)

    def initInfo(self, txt):
        self.originText = txt
        self.finalText = ""
        self.wp_textContent.setPlainText(txt)

    def getInfo(self):
        return self.finalText

    def save(self):
        self.finalText = self.wp_textContent.toPlainText()
        self.accept()

    def cancel(self):
        self.finalText = self.originText
        self.reject()