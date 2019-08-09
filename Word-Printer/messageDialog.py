# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QMessageBox
from PyQt5.QtCore import QDate, QThread

class MessageDialog(QMessageBox):

    def showErrorDialog(self, title, content):
        reply = QMessageBox.critical(self, title, content, QMessageBox.Yes | QMessageBox.Cancel)

    def showInformationDialog(self, title, content):
        reply = QMessageBox.information(self, title, content, QMessageBox.Ok)

    def showWarningDialog(self, title, content):
        reply = QMessageBox.warning(self, title, content, QMessageBox.Yes | QMessageBox.Cancel)

    def showWarningDialogWithMethod(self, title, content, yesMethod, cancelMethod=None):
        reply = QMessageBox.warning(self, title, content, QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            if yesMethod:
                yesMethod()
        else:
            if cancelMethod:
                cancelMethod()