from test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog

class Controller(QMainWindow, Ui_MainWindow):
    name = ''

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.Init()
        self.level1Border.clicked.connect(lambda: self.showDialog(self.level1Border))

    def Init(self):
        self.addressText.setText("Test case")

    def showDialog(self, tar): 
        col = QColorDialog.getColor() 
        print(col.name(),"\n")
        if col.isValid(): 
            tar.setStyleSheet('QWidget {background-color:%s}'%col.name()) 