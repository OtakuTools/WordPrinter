from test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from dataStruct import userInfo

class Controller(QMainWindow, Ui_MainWindow):
    user = userInfo()

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectButton()
        self.connectText()
        #self.setUser()
        #self.level1Border.clicked.connect(lambda: self.showDialog(self.level1Border))
        #self.fileNameText.textChanged.connect( lambda:self.plainTextEdit_2.setPlainText( self.fileNameText.text() ) )
    
    def showDialog(self, tar): 
        col = QColorDialog.getColor() 
        print(col.name(),"\n")
        if col.isValid(): 
            tar.setStyleSheet('QWidget {background-color:%s}'%col.name())

    def getInfo():
        return user

    def connectText(self):
        self.fileNameText.textChanged.connect( lambda : self.setUser() )
        self.companyText.textChanged.connect( lambda : self.setUser() )
        self.addressText.textChanged.connect( lambda : self.setUser() )
        self.coverFieldText.textChanged.connect( lambda : self.setUser() )
        self.managerText.textChanged.connect( lambda : self.setUser() )
        self.guandaiText.textChanged.connect( lambda : self.setUser() )
        self.employeesText.textChanged.connect( lambda : self.setUser() )
        self.approverText.textChanged.connect( lambda : self.setUser() )
        self.auditText.textChanged.connect( lambda : self.setUser() )
        self.announcerText.textChanged.connect( lambda : self.setUser() )
        self.zipText.textChanged.connect( lambda : self.setUser() )
        self.phoneText.textChanged.connect( lambda : self.setUser() )
        self.policyText.textChanged.connect( lambda : self.setUser() )
        #self.fileNameText.textChanged.connect( lambda : self.setUser() )

    def connectButton(self):

        #deStructBorderColor
        self.level1Border.clicked.connect(lambda: self.showDialog(self.level1Border))
        self.level2Border.clicked.connect(lambda: self.showDialog(self.level2Border))
        self.level3Border.clicked.connect(lambda: self.showDialog(self.level3Border))
        self.level4Border.clicked.connect(lambda: self.showDialog(self.level4Border))

        #deStructFontColor
        self.level1Font.clicked.connect(lambda: self.showDialog(self.level1Font))
        self.level2Font.clicked.connect(lambda: self.showDialog(self.level2Font))
        self.level3Font.clicked.connect(lambda: self.showDialog(self.level3Font))
        self.level4Font.clicked.connect(lambda: self.showDialog(self.level4Font))

        #preview
        self.createBotton.clicked.connect( lambda: self.plainTextEdit_2.setPlainText( str(vars(self.user)) ) )

    def setUser(self):
        self.user.fileName=self.fileNameText.text()
        self.user.company=self.companyText.text()
        self.user.address=self.addressText.text()
        self.user.coverField=self.coverFieldText.text()
        self.user.manager=self.managerText.text()
        self.user.guandai=self.guandaiText.text()
        self.user.employees=self.employeesText.text()
        self.user.approver=self.approverText.text()
        self.user.audit=self.auditText.text()
        self.user.announcer=self.announcerText.text()
        self.user.zip=self.zipText.text()
        self.user.phone=self.phoneText.text()
        self.user.policy=self.policyText.text()
